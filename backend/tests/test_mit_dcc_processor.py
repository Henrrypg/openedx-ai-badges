"""
Tests for MITDCCProcessor.

Covers:
- _build_course_input: field assembly and empty-field handling
- _parse_api_response: badge extraction paths, skills normalisation,
  extra-key preservation
- generate_badge (mock path): output shape matches parsed real-API shape
- generate_badge (real API path via mocked requests): happy path and all
  error conditions
"""
from unittest.mock import MagicMock, patch

import pytest
from django.conf import settings

from openedx_ai_badges.processors.mit_dcc_processor import MITDCCProcessor


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

COURSE_CONTEXT = {
    "title": "Intro to Python",
    "short_description": "Learn Python basics.",
    "description": "A hands-on Python course.",
    "overview": "<p>Overview HTML</p>",
}

INPUT_DATA_NO_SKILLS = {
    "style": "modern",
    "tone": "professional",
    "level": "beginner",
    "criterion": "completion",
    "skillsEnabled": False,
}

INPUT_DATA_WITH_SKILLS = {**INPUT_DATA_NO_SKILLS, "skillsEnabled": True}

# Exact shape the real API returns (captured from live logs)
REAL_API_RESPONSE = {
    "credentialSubject": {
        "achievement": {
            "name": "Intro to Python — Beginner Badge",
            "description": "Awarded for completion of Intro to Python.",
            "criteria": {"narrative": "Earners have demonstrated completion at beginner level."},
        }
    },
    "imageConfig": None,
    "badge_id": "17acfd88-56ae-4a18-a427-4d219445b704",
    "metrics": {
        "total_duration": 5463326822,
        "load_duration": 235142373,
        "prompt_eval_count": 1398,
        "prompt_eval_duration": 12583359,
        "eval_count": 295,
        "eval_duration": 4320496623,
    },
    "skills": [
        {
            "Knowledge Required": [],
            "Task Abilities": [],
            "Skill Tag": "ESCO.474",
            "Correlation Coefficient": 0.59,
            "targetName": "E-Learning",
            "targetDescription": "Strategies using ICT for learning.",
            "targetUrl": "http://data.europa.eu/esco/skill/5f5e9350-1d13-4391-b9e1-07f6b2047fc5",
            "type": "Alignment",
            "targetType": "ESCO:Skill",
        }
    ],
    "badge_configuration": {
        "badge_style": "modern",
        "badge_tone": "professional",
        "criterion_style": "completion",
        "badge_level": "beginner",
        "institution": "",
        "institute_url": "",
        "custom_instructions": "",
    },
    "enable_image_generation": False,
    "enable_skill_extraction": True,
}


@pytest.fixture
def processor():
    return MITDCCProcessor(processor_config={})


# ---------------------------------------------------------------------------
# _build_course_input
# ---------------------------------------------------------------------------

class TestBuildCourseInput:
    def test_all_fields_joined(self, processor):
        result = processor._build_course_input(COURSE_CONTEXT)
        assert "Intro to Python" in result
        assert "Learn Python basics." in result
        assert "A hands-on Python course." in result
        assert "Overview HTML" in result

    def test_empty_fields_skipped(self, processor):
        ctx = {"title": "My Course", "short_description": "", "description": None, "overview": "  "}
        result = processor._build_course_input(ctx)
        assert result == "My Course"

    def test_missing_title(self, processor):
        ctx = {"short_description": "Short desc."}
        result = processor._build_course_input(ctx)
        assert result == "Short desc."

    def test_empty_context(self, processor):
        assert processor._build_course_input({}) == ""


# ---------------------------------------------------------------------------
# _parse_api_response
# ---------------------------------------------------------------------------

class TestParseApiResponse:
    def test_badge_extracted_from_achievement(self, processor):
        result = processor._parse_api_response(REAL_API_RESPONSE, skills_enabled=True)
        assert result["badge"] == REAL_API_RESPONSE["credentialSubject"]["achievement"]

    def test_badge_falls_back_to_credential_subject_when_no_achievement(self, processor):
        data = {
            "credentialSubject": {"name": "Direct Badge"},
            "badge_id": "abc",
        }
        result = processor._parse_api_response(data, skills_enabled=False)
        assert result["badge"] == {"name": "Direct Badge"}

    def test_badge_falls_back_to_full_response_when_no_credential_subject(self, processor):
        data = {"name": "Flat Badge", "badge_id": "abc"}
        result = processor._parse_api_response(data, skills_enabled=False)
        assert result["badge"] == data

    def test_skills_list_wrapped_in_alignment_envelope(self, processor):
        result = processor._parse_api_response(REAL_API_RESPONSE, skills_enabled=True)
        assert "skills" in result
        assert "alignment" in result["skills"]
        assert isinstance(result["skills"]["alignment"], list)
        assert len(result["skills"]["alignment"]) == 1

    def test_skills_dict_passed_through(self, processor):
        data = {
            "credentialSubject": {"achievement": {"name": "B"}},
            "skills": {"alignment": [{"targetName": "X"}]},
        }
        result = processor._parse_api_response(data, skills_enabled=True)
        assert result["skills"] == {"alignment": [{"targetName": "X"}]}

    def test_skills_stored_even_when_disabled(self, processor):
        result = processor._parse_api_response(REAL_API_RESPONSE, skills_enabled=False)
        assert "skills" in result
        assert "alignment" in result["skills"]

    def test_skills_absent_when_disabled_and_not_in_response(self, processor):
        data = {
            "credentialSubject": {"achievement": {"name": "B"}},
            "badge_id": "abc",
        }
        result = processor._parse_api_response(data, skills_enabled=False)
        assert "skills" not in result

    def test_extra_keys_namespaced(self, processor):
        result = processor._parse_api_response(REAL_API_RESPONSE, skills_enabled=True)
        assert "mit_dcc_badge_id" in result
        assert result["mit_dcc_badge_id"] == REAL_API_RESPONSE["badge_id"]
        assert "mit_dcc_metrics" in result
        assert result["mit_dcc_metrics"] == REAL_API_RESPONSE["metrics"]
        assert "mit_dcc_imageConfig" in result
        assert "mit_dcc_badge_configuration" in result
        assert "mit_dcc_enable_image_generation" in result
        assert "mit_dcc_enable_skill_extraction" in result

    def test_credential_subject_not_in_extras(self, processor):
        result = processor._parse_api_response(REAL_API_RESPONSE, skills_enabled=False)
        assert "mit_dcc_credentialSubject" not in result
        assert "mit_dcc_skills" not in result


# ---------------------------------------------------------------------------
# generate_badge — mock path
# ---------------------------------------------------------------------------

class TestGenerateBadgeMock:
    def test_returns_badge_key(self, processor):
        result = processor._mock_api_response(COURSE_CONTEXT, INPUT_DATA_NO_SKILLS)
        assert "badge" in result
        assert result["badge"]["name"] == "Intro to Python — Beginner Badge"

    def test_returns_skills_when_enabled(self, processor):
        result = processor._mock_api_response(COURSE_CONTEXT, INPUT_DATA_WITH_SKILLS)
        assert "skills" in result
        assert "alignment" in result["skills"]
        assert len(result["skills"]["alignment"]) > 0

    def test_skills_stored_even_when_disabled(self, processor):
        # mock always includes skills in raw payload, even when disabled
        result = processor._mock_api_response(COURSE_CONTEXT, INPUT_DATA_NO_SKILLS)
        assert "skills" in result

    def test_extra_mit_dcc_keys_present(self, processor):
        result = processor._mock_api_response(COURSE_CONTEXT, INPUT_DATA_NO_SKILLS)
        assert "mit_dcc_badge_id" in result
        assert "mit_dcc_metrics" in result
        assert "mit_dcc_badge_configuration" in result

    def test_mock_and_real_produce_same_top_level_shape(self, processor):
        mock_result = processor._mock_api_response(COURSE_CONTEXT, INPUT_DATA_WITH_SKILLS)
        real_result = processor._parse_api_response(REAL_API_RESPONSE, skills_enabled=True)
        assert set(mock_result.keys()) == set(real_result.keys())

    def test_badge_contains_name_description_criteria(self, processor):
        result = processor._mock_api_response(COURSE_CONTEXT, INPUT_DATA_NO_SKILLS)
        badge = result["badge"]
        assert "name" in badge
        assert "description" in badge
        assert "criteria" in badge
        assert "narrative" in badge["criteria"]


# ---------------------------------------------------------------------------
# generate_badge — real API path (requests mocked)
# ---------------------------------------------------------------------------

class TestGenerateBadgeCallApi:
    def _make_mock_response(self, json_data=None, status_code=200):
        mock_resp = MagicMock()
        mock_resp.status_code = status_code
        mock_resp.headers = {"content-type": "application/json", "content-length": "100"}
        mock_resp.text = str(json_data)
        mock_resp.json.return_value = json_data or REAL_API_RESPONSE
        mock_resp.raise_for_status = MagicMock()
        return mock_resp

    @patch("openedx_ai_badges.processors.mit_dcc_processor.requests.post")
    def test_happy_path_returns_normalised_result(self, mock_post, processor):
        mock_post.return_value = self._make_mock_response(REAL_API_RESPONSE)
        result = processor._call_api(COURSE_CONTEXT, INPUT_DATA_WITH_SKILLS)
        assert "badge" in result
        assert "skills" in result
        assert "mit_dcc_badge_id" in result
        assert result["mit_dcc_badge_id"] == "17acfd88-56ae-4a18-a427-4d219445b704"

    @patch("openedx_ai_badges.processors.mit_dcc_processor.requests.post")
    def test_correct_payload_sent(self, mock_post, processor):
        mock_post.return_value = self._make_mock_response(REAL_API_RESPONSE)
        processor._call_api(COURSE_CONTEXT, INPUT_DATA_WITH_SKILLS)
        _, kwargs = mock_post.call_args
        payload = kwargs["json"]
        assert payload["badge_configuration"]["badge_style"] == "modern"
        assert payload["badge_configuration"]["badge_tone"] == "professional"
        assert payload["badge_configuration"]["badge_level"] == "beginner"
        assert payload["badge_configuration"]["criterion_style"] == "completion"
        assert payload["enable_skill_extraction"] is True
        assert payload["image_generation"] == {"enabled": False}

    @patch("openedx_ai_badges.processors.mit_dcc_processor.requests.post")
    def test_uses_default_api_url(self, mock_post, processor):
        mock_post.return_value = self._make_mock_response(REAL_API_RESPONSE)
        processor._call_api(COURSE_CONTEXT, INPUT_DATA_NO_SKILLS)
        args, _ = mock_post.call_args
        assert args[0] == settings.MIT_DCC_BADGE_API_URL

    @patch("openedx_ai_badges.processors.mit_dcc_processor.requests.post")
    def test_connection_error_returns_error_dict(self, mock_post, processor):
        import requests as req
        mock_post.side_effect = req.exceptions.ConnectionError("refused")
        result = processor._call_api(COURSE_CONTEXT, INPUT_DATA_NO_SKILLS)
        assert "error" in result
        assert "refused" in result["error"]

    @patch("openedx_ai_badges.processors.mit_dcc_processor.requests.post")
    def test_timeout_returns_error_dict(self, mock_post, processor):
        import requests as req
        mock_post.side_effect = req.exceptions.Timeout("timed out")
        result = processor._call_api(COURSE_CONTEXT, INPUT_DATA_NO_SKILLS)
        assert "error" in result
        assert "timed out" in result["error"]

    @patch("openedx_ai_badges.processors.mit_dcc_processor.requests.post")
    def test_http_error_returns_error_dict(self, mock_post, processor):
        import requests as req
        mock_resp = self._make_mock_response(status_code=500)
        mock_resp.raise_for_status.side_effect = req.exceptions.HTTPError("500 Server Error")
        mock_post.return_value = mock_resp
        result = processor._call_api(COURSE_CONTEXT, INPUT_DATA_NO_SKILLS)
        assert "error" in result

    @patch("openedx_ai_badges.processors.mit_dcc_processor.requests.post")
    def test_invalid_json_returns_error_dict(self, mock_post, processor):
        mock_resp = self._make_mock_response()
        mock_resp.json.side_effect = ValueError("not json")
        mock_post.return_value = mock_resp
        result = processor._call_api(COURSE_CONTEXT, INPUT_DATA_NO_SKILLS)
        assert "error" in result
        assert "Invalid JSON" in result["error"]

    @patch("openedx_ai_badges.processors.mit_dcc_processor.requests.post")
    def test_skills_snake_case_alias_accepted(self, mock_post, processor):
        mock_post.return_value = self._make_mock_response(REAL_API_RESPONSE)
        input_data = {**INPUT_DATA_NO_SKILLS, "skills_enabled": True}
        input_data.pop("skillsEnabled", None)
        result = processor._call_api(COURSE_CONTEXT, input_data)
        assert "skills" in result


# ---------------------------------------------------------------------------
# api_url setting override
# ---------------------------------------------------------------------------

class TestApiUrlSetting:
    def test_default_url(self, processor):
        assert processor.api_url == settings.MIT_DCC_BADGE_API_URL

    @patch("openedx_ai_badges.processors.mit_dcc_processor.settings")
    def test_overridden_by_django_setting(self, mock_settings, processor):
        mock_settings.MIT_DCC_BADGE_API_URL = "http://localhost:8599/api/v1/generate-badge-suggestions"
        assert processor.api_url == "http://localhost:8599/api/v1/generate-badge-suggestions"
