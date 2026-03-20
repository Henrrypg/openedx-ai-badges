MIT SLM Orchestrator
####################

.. contents::
   :local:
   :depth: 2

Overview
********

The MIT SLM integration introduces a second badge-generation backend: instead of
calling an LLM provider directly from inside Open edX (as the default
``BadgeOrchestrator`` does), it delegates to an external HTTP micro-service —
the **MIT DCC Badge API** — which internally runs a fine-tuned small language
model and a dedicated skill-extraction model.

This approach is experimental and is aimed at evaluating self-hosted, fine-tuned
models as an alternative to general-purpose cloud LLMs for structured badge
generation.


Services Involved
*****************

MIT DCC Badge API
=================

A Python HTTP service based on `oneorigin-inc/mit-slm
<https://github.com/oneorigin-inc/mit-slm>`_, modified to support running Ollama
on Hugging Face Spaces (see `PR #18
<https://github.com/oneorigin-inc/mit-slm/pull/18>`_). It exposes a ``POST``
endpoint that accepts a course description and badge configuration options and
returns a structured badge definition.

Internally the API:

1. Calls an Ollama instance to run the fine-tuned ``phi4-chat`` model for badge
   generation.
2. Optionally calls the **LAiSER** skill-extraction model to map the course
   content to ESCO skill taxonomy entries.

The Docker image currently used is ``felipemontoya/dcc-mit-badge-api:latest``,
which was built from the repository above and pushed to a personal registry by
Felipe Montoya. This is the reference image for now, but it is subject to
change. If the upstream project establishes its own maintained image, that
should be preferred over this personal build.

LAiSER (skill extraction)
=========================

`LAiSER <https://laiser.gwu.edu/>`_ is a project from George Washington
University. It uses AI to identify skills from human-readable text, linking them
to an evolving skills database. This helps individuals showcase their talents and
organizations find the right talent more easily.

When skill extraction is enabled (``skillsEnabled = true`` in the badge form),
the MIT DCC Badge API calls the LAiSER model to produce a list of ESCO-tagged
skill alignments that are bundled into the final badge definition.


Architecture
************

The diagram below shows how the components interact when a badge is generated
via the MIT SLM orchestrator::

    Open edX (LMS/CMS)
    │
    ├─ OpenEdXProcessor          # Extracts course title, description, overview
    │
    └─ MITDCCBadgeOrchestrator  # Delegates to remote API
        │
        └─► MIT DCC Badge API (HTTP POST /generate)
               │
               ├─► Ollama / phi4-chat   # Badge JSON generation
               │
               └─► LAiSER model         # ESCO skill extraction (optional)


Compared to the Default Orchestrator
*************************************

+-------------------------------+------------------------------------------+------------------------------------------+
|                               | ``BadgeOrchestrator``                    | ``MITDCCBadgeOrchestrator``              |
+===============================+==========================================+==========================================+
| **LLM access**                | Direct, via ``litellm`` (any provider    | Indirect, via MIT DCC Badge API HTTP     |
|                               | configured in the AI profile)            | service                                  |
+-------------------------------+------------------------------------------+------------------------------------------+
| **Badge generation model**    | Configured by the AI profile             | phi4-chat (fine-tuned), hosted in Ollama |
+-------------------------------+------------------------------------------+------------------------------------------+
| **Skill extraction**          | ``SkillsProcessor`` (same LLM provider)  | LAiSER model (inside the remote service) |
+-------------------------------+------------------------------------------+------------------------------------------+
| **Infrastructure requirement**| An LLM provider API key or endpoint      | MIT DCC Badge API + Ollama instance      |
+-------------------------------+------------------------------------------+------------------------------------------+
| **Response parsing**          | Parses LLM output with JSON schema       | Parses API JSON, normalises into the     |
|                               | enforcement                              | same internal shape                      |
+-------------------------------+------------------------------------------+------------------------------------------+
| **Service status check**      | Not applicable                           | ``get_api_status`` action checks both    |
|                               |                                          | the Badge API and Ollama health          |
+-------------------------------+------------------------------------------+------------------------------------------+

Both orchestrators produce the same output shape (``badge``, optional ``skills``,
``course_context``) and share the same ``save``, ``regenerate``, and
``regenerate_async`` actions, so the frontend UI works unchanged with either.


Deployment Options
******************

There are two independent pieces of infrastructure to deploy:

1. The **MIT DCC Badge API** service (controlled by ``RUN_MIT_SLM``).
2. An **Ollama** instance serving the phi4-chat fine-tune (configured via
   ``MIT_SLM_OLLAMA_URL``). This is a separate concern and is not managed by
   this plugin.

MIT DCC Badge API sidecar (``RUN_MIT_SLM=true``)
=================================================

Setting ``RUN_MIT_SLM=true`` deploys the MIT DCC Badge API as a Docker Compose
service (or Kubernetes deployment) running alongside Open edX::

    tutor config save --set RUN_MIT_SLM=true
    tutor local launch

The service is named ``mit-slm`` and is reachable at ``http://mit-slm:8000``
from inside the Open edX containers. It still requires a separate Ollama
instance; point ``MIT_SLM_OLLAMA_URL`` to wherever that is hosted.

Ollama hosting
==============

The default ``MIT_SLM_OLLAMA_URL`` points to a reference Hugging Face Space
(``felipemontoya-mit-dcc-ollama``), which is convenient for quick evaluation.

For any deployment beyond local development, the right choice of Ollama hosting
depends on the compliance requirements, cost constraints, and infrastructure
preferences of whoever is operating the platform. Running Ollama in the same
cluster is one option, but it is not necessarily the most cost-efficient or
compliant one. Evaluate the available options — managed GPU cloud services,
Hugging Face Inference Endpoints, in-cluster deployment — and choose the one
that best fits your context.


Configuration
*************

All variables are Tutor config keys. Set them with ``tutor config save --set``.

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - Variable
     - Default
     - Description
   * - ``RUN_MIT_SLM``
     - ``false``
     - Deploy the MIT DCC Badge API sidecar service.
   * - ``MIT_SLM_DOCKER_IMAGE``
     - ``felipemontoya/dcc-mit-badge-api:latest``
     - Docker image for the sidecar service.
   * - ``MIT_SLM_OLLAMA_URL``
     - HF Space URL
     - Full URL to the Ollama ``/api/generate`` endpoint used by the Badge API.
   * - ``MIT_SLM_OLLAMA_TOKEN``
     - *(empty)*
     - Bearer token for protected Ollama endpoints.
   * - ``MIT_SLM_MODEL_NAME``
     - ``phi4-chat``
     - Model name passed to Ollama.
   * - ``MIT_SLM_OLLAMA_PRELOAD``
     - ``false``
     - Pre-load the model into memory on service startup.
   * - ``MIT_DCC_BADGE_API_HEALTH_URL``
     - ``http://mit-slm:8000/health``
     - Health check URL shown in the UI status panel.

The following Django settings are injected into Open edX via the
``openedx-common-settings`` patch:

- ``MIT_SLM_OLLAMA_URL``
- ``MIT_SLM_OLLAMA_TOKEN``
- ``MIT_DCC_BADGE_API_HEALTH_URL``

The ``MIT_DCC_BADGE_API_URL`` setting (the endpoint the orchestrator calls) must
be set separately in Django settings and is not managed by the Tutor plugin at
this time.


Setup Steps
***********

1. **Enable the sidecar and configure Ollama**::

       tutor config save --set RUN_MIT_SLM=true
       tutor config save --set MIT_SLM_OLLAMA_URL="<your-ollama-endpoint>"

2. **Rebuild and relaunch**::

       tutor images build openedx
       tutor local launch

3. **Create an AI Profile** in the Django Admin using the provided profile
   definition, or create one manually with:

   - *Orchestrator class*: ``openedx_ai_badges.workflows.orchestrators.MITDCCBadgeOrchestrator``
   - *Processor config*: see ``backend/openedx_ai_badges/workflows/profiles/mit_dcc_badges.json``

4. **Assign a Scope** to this profile (e.g. CMS) and navigate to
   *Pages and Resources > AI Extensions Settings > AI Badges* to use it.
