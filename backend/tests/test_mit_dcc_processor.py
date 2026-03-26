"""
Tests for MITDCCProcessor.

Covers:
- _build_course_input: field assembly and empty-field handling
- _parse_api_response: canonical pass-through, warnings on missing keys
- generate_badge (mock path): canonical shape is returned unchanged
- generate_badge (real API path via mocked requests): happy path and all
  error conditions
"""
# pylint: disable=protected-access,redefined-outer-name
from unittest.mock import MagicMock, patch

import pytest
import requests as req
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
    """Return a bare MITDCCProcessor instance."""
    return MITDCCProcessor(processor_config={})


# ---------------------------------------------------------------------------
# _build_course_input
# ---------------------------------------------------------------------------

class TestBuildCourseInput:
    """Tests for MITDCCProcessor._build_course_input."""

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
    """Tests for MITDCCProcessor._parse_api_response — canonical pass-through."""

    def test_returns_data_unchanged(self, processor):
        result = processor._parse_api_response(REAL_API_RESPONSE, skills_enabled=True)
        assert result is REAL_API_RESPONSE

    def test_credential_subject_preserved(self, processor):
        result = processor._parse_api_response(REAL_API_RESPONSE, skills_enabled=True)
        assert result["credentialSubject"] == REAL_API_RESPONSE["credentialSubject"]
        assert result["credentialSubject"]["achievement"]["name"] == "Intro to Python — Beginner Badge"

    def test_skills_list_preserved(self, processor):
        result = processor._parse_api_response(REAL_API_RESPONSE, skills_enabled=True)
        assert isinstance(result["skills"], list)
        assert len(result["skills"]) == 1
        assert result["skills"][0]["targetName"] == "E-Learning"

    def test_top_level_metadata_preserved(self, processor):
        result = processor._parse_api_response(REAL_API_RESPONSE, skills_enabled=True)
        assert result["badge_id"] == "17acfd88-56ae-4a18-a427-4d219445b704"
        assert result["badge_configuration"]["badge_style"] == "modern"
        assert result["imageConfig"] is None

    def test_warns_on_missing_credential_subject(self, processor):
        data = {"badge_id": "abc"}
        with patch('openedx_ai_badges.processors.mit_dcc_processor.logger') as mock_logger:
            processor._parse_api_response(data, skills_enabled=False)
            mock_logger.warning.assert_called()

    def test_warns_on_missing_skills_when_enabled(self, processor):
        data = {"credentialSubject": {"achievement": {"name": "B"}}}
        with patch('openedx_ai_badges.processors.mit_dcc_processor.logger') as mock_logger:
            processor._parse_api_response(data, skills_enabled=True)
            warning_calls = [str(c) for c in mock_logger.warning.call_args_list]
            assert any("skills" in w for w in warning_calls)

    def test_no_warning_when_skills_disabled_and_absent(self, processor):
        data = {"credentialSubject": {"achievement": {"name": "B"}}}
        with patch('openedx_ai_badges.processors.mit_dcc_processor.logger') as mock_logger:
            processor._parse_api_response(data, skills_enabled=False)
            warning_calls = [str(c) for c in mock_logger.warning.call_args_list]
            assert not any("skills" in w for w in warning_calls)


# ---------------------------------------------------------------------------
# generate_badge — mock path
# ---------------------------------------------------------------------------

class TestGenerateBadgeMock:
    """Tests for MITDCCProcessor._mock_api_response — canonical shape."""

    def test_returns_credential_subject(self, processor):
        result = processor._mock_api_response(COURSE_CONTEXT, INPUT_DATA_NO_SKILLS)
        assert "credentialSubject" in result
        assert "achievement" in result["credentialSubject"]

    def test_achievement_contains_required_fields(self, processor):
        result = processor._mock_api_response(COURSE_CONTEXT, INPUT_DATA_NO_SKILLS)
        achievement = result["credentialSubject"]["achievement"]
        assert "name" in achievement
        assert "description" in achievement
        assert "criteria" in achievement
        assert "narrative" in achievement["criteria"]

    def test_returns_skills_list(self, processor):
        result = processor._mock_api_response(COURSE_CONTEXT, INPUT_DATA_WITH_SKILLS)
        assert "skills" in result
        assert isinstance(result["skills"], list)
        assert len(result["skills"]) > 0

    def test_badge_configuration_present(self, processor):
        result = processor._mock_api_response(COURSE_CONTEXT, INPUT_DATA_NO_SKILLS)
        assert "badge_configuration" in result
        assert result["badge_configuration"]["badge_style"] == "modern"

    def test_metadata_fields_present(self, processor):
        result = processor._mock_api_response(COURSE_CONTEXT, INPUT_DATA_NO_SKILLS)
        assert "badge_id" in result
        assert "metrics" in result
        assert "imageConfig" in result

    def test_mock_and_real_produce_same_top_level_keys(self, processor):
        mock_result = processor._mock_api_response(COURSE_CONTEXT, INPUT_DATA_WITH_SKILLS)
        assert set(mock_result.keys()) == set(REAL_API_RESPONSE.keys())

    def test_no_legacy_badge_key(self, processor):
        result = processor._mock_api_response(COURSE_CONTEXT, INPUT_DATA_NO_SKILLS)
        assert "badge" not in result

    def test_no_mit_dcc_namespaced_keys(self, processor):
        result = processor._mock_api_response(COURSE_CONTEXT, INPUT_DATA_NO_SKILLS)
        assert not any(k.startswith("mit_dcc_") for k in result)


# ---------------------------------------------------------------------------
# generate_badge — real API path (requests mocked)
# ---------------------------------------------------------------------------

class TestGenerateBadgeCallApi:
    """Tests for MITDCCProcessor._call_api with mocked HTTP."""

    def _make_mock_response(self, json_data=None, status_code=200):
        """Return a MagicMock mimicking a requests.Response."""
        mock_resp = MagicMock()
        mock_resp.status_code = status_code
        mock_resp.headers = {"content-type": "application/json", "content-length": "100"}
        mock_resp.text = str(json_data)
        mock_resp.json.return_value = json_data or REAL_API_RESPONSE
        mock_resp.raise_for_status = MagicMock()
        return mock_resp

    @patch("openedx_ai_badges.processors.mit_dcc_processor.requests.post")
    def test_happy_path_returns_canonical_result(self, mock_post, processor):
        mock_post.return_value = self._make_mock_response(REAL_API_RESPONSE)
        result = processor._call_api(COURSE_CONTEXT, INPUT_DATA_WITH_SKILLS)
        assert "credentialSubject" in result
        assert "skills" in result
        assert "badge_id" in result
        assert result["badge_id"] == "17acfd88-56ae-4a18-a427-4d219445b704"

    @patch("openedx_ai_badges.processors.mit_dcc_processor.requests.post")
    def test_no_legacy_keys_in_result(self, mock_post, processor):
        mock_post.return_value = self._make_mock_response(REAL_API_RESPONSE)
        result = processor._call_api(COURSE_CONTEXT, INPUT_DATA_WITH_SKILLS)
        assert "badge" not in result
        assert not any(k.startswith("mit_dcc_") for k in result)

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
        mock_post.side_effect = req.exceptions.ConnectionError("refused")
        result = processor._call_api(COURSE_CONTEXT, INPUT_DATA_NO_SKILLS)
        assert "error" in result
        assert "refused" in result["error"]

    @patch("openedx_ai_badges.processors.mit_dcc_processor.requests.post")
    def test_timeout_returns_error_dict(self, mock_post, processor):
        mock_post.side_effect = req.exceptions.Timeout("timed out")
        result = processor._call_api(COURSE_CONTEXT, INPUT_DATA_NO_SKILLS)
        assert "error" in result
        assert "timed out" in result["error"]

    @patch("openedx_ai_badges.processors.mit_dcc_processor.requests.post")
    def test_http_error_returns_error_dict(self, mock_post, processor):
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
    """Tests for MITDCCProcessor.api_url Django settings integration."""

    def test_default_url(self, processor):
        assert processor.api_url == settings.MIT_DCC_BADGE_API_URL

    @patch("openedx_ai_badges.processors.mit_dcc_processor.settings")
    def test_overridden_by_django_setting(self, mock_settings, processor):
        mock_settings.MIT_DCC_BADGE_API_URL = "http://localhost:8599/api/v1/generate-badge-suggestions"
        assert processor.api_url == "http://localhost:8599/api/v1/generate-badge-suggestions"
