"""
Data classes for openedx-ai-badges local events.

``BadgeTemplateData`` (from openedx-events) covers uuid/origin/name/description/image_url
but has no ``course_id`` or ``criteria_narrative``.  ``BadgeData`` adds a ``UserData``
(learner PII) which is wrong for a course-level event.

``BadgeGenerationData`` extends the template concept with those two missing fields.
It follows OEP-49 (frozen attrs) so it can be contributed to openedx/openedx-events later.

Once accepted upstream, replace these imports with:
    from openedx_events.learning.data import BadgeGenerationData
"""
import attr
from opaque_keys.edx.keys import CourseKey


@attr.s(frozen=True)
class BadgeGenerationData:
    """
    Data for the BADGE_GENERATION event.

    Extends the concept of ``BadgeTemplateData`` (openedx-events) adding
    ``course_id`` and ``criteria_narrative``, which are missing from that class.
    Carries no user/learner information — this is a course-level artifact.

    Attributes:
        uuid (str): Unique identifier for this generation event (UUID v4).
        course_id (CourseKey): The course for which the badge was generated.
        name (str): Human-readable badge name.
        origin (str): Identifier of the system that generated the badge.
        description (str): What the badge represents.
        criteria_narrative (str): Open Badges 3.0 ``criteria.narrative`` text.
        image_url (str): URL or data-URI of the badge image.
    """

    uuid = attr.ib(type=str)
    course_id = attr.ib(type=CourseKey)
    name = attr.ib(type=str)
    origin = attr.ib(type=str, default="openedx-ai-badges")
    description = attr.ib(type=str, default="")
    criteria_narrative = attr.ib(type=str, default="")
    image_url = attr.ib(type=str, default="")
