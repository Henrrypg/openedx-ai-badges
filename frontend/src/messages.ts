import { defineMessages } from '@edx/frontend-platform/i18n';

const messages = defineMessages({
  // Profile loading / no-config states
  'openedx-ai-badges.profile.loading': {
    id: 'openedx-ai-badges.profile.loading',
    defaultMessage: 'Loading badge workflow configuration…',
    description: 'Shown while the profile endpoint is being fetched',
  },
  'openedx-ai-badges.profile.no-config': {
    id: 'openedx-ai-badges.profile.no-config',
    defaultMessage: 'No badge workflow is configured for this course.',
    description: 'Shown when the profile endpoint returns no configuration',
  },

  'openedx-ai-badges.badge-form.button.regenerate': {
    id: 'openedx-ai-badges.badge-form.button.regenerate',
    defaultMessage: 'Regenerate badge',
    description: 'Button to regenerate an existing badge',
  },
  'openedx-ai-badges.badge-form.generating.message': {
    id: 'openedx-ai-badges.badge-form.generating.message',
    defaultMessage: 'Please wait while AI creates your badge',
    description: 'Message shown during generation',
  },
  'openedx-ai-badges.badge-form.regenerating.message': {
    id: 'openedx-ai-badges.badge-form.regenerating.message',
    defaultMessage: 'Please wait while AI regenerates your badge',
    description: 'Message shown during regeneration',
  },
  'openedx-ai-badges.badge-form.error.required-field': {
    id: 'openedx-ai-badges.badge-form.error.required-field',
    defaultMessage: 'This field is required',
    description: 'Error for required field',
  },

  // Badge Preview Placeholder
  'openedx-ai-badges.badge-preview.placeholder': {
    id: 'openedx-ai-badges.badge-preview.placeholder',
    defaultMessage: 'Your badge preview will appear here',
    description: 'Placeholder text shown in the preview panel before a badge is generated',
  },

  // Missing messages for AIBadgesTab
  'openedx-ai-badges.badge-form.header': {
    id: 'openedx-ai-badges.badge-form.header',
    defaultMessage: 'Badge Generator',
    description: 'Header for the badge generator form',
  },
  'openedx-ai-badges.badge-form.description': {
    id: 'openedx-ai-badges.badge-form.description',
    defaultMessage: 'This tab allows you to generate <bold>Open Badges 3.0</bold> following the official standard. The system automatically extracts real information from your course, including the title, description, and overview by default. <br></br> The extraction process and the final output are highly configurable via the <bold>AI Workflow Profile</bold>.',
    description: 'First paragraph of the badge generator description',
  },
  'openedx-ai-badges.badge-form.skills.description.short': {
    id: 'openedx-ai-badges.badge-form.skills.description.short',
    defaultMessage: 'Automatically extract and align skills from the badge',
    description: 'Short description for skill extraction toggle',
  },
  'openedx-ai-badges.badge-preview.course-context.title': {
    id: 'openedx-ai-badges.badge-preview.course-context.title',
    defaultMessage: 'Course Context',
    description: 'Title for the course context section in the preview',
  },
  'openedx-ai-badges.badge-preview.skills.title': {
    id: 'openedx-ai-badges.badge-preview.skills.title',
    defaultMessage: 'Skills',
    description: 'Title for the skills section in the preview',
  },
  'openedx-ai-badges.badge-preview.badge.title': {
    id: 'openedx-ai-badges.badge-preview.badge.title',
    defaultMessage: 'Badge',
    description: 'Title for the badge section in the preview',
  },
  'openedx-ai-badges.badge-preview.save.button': {
    id: 'openedx-ai-badges.badge-preview.save.button',
    defaultMessage: 'Save',
    description: 'Button label for saving a badge section',
  },
  'openedx-ai-badges.badge-preview.edit.aria-label': {
    id: 'openedx-ai-badges.badge-preview.edit.aria-label',
    defaultMessage: 'Edit {section} JSON',
    description: 'Aria label for the JSON editor textarea',
  },
  'openedx-ai-badges.badge-preview.edit.button': {
    id: 'openedx-ai-badges.badge-preview.edit.button',
    defaultMessage: 'Edit',
    description: 'Label for the edit button',
  },
  'openedx-ai-badges.badge-preview.edit.button.aria': {
    id: 'openedx-ai-badges.badge-preview.edit.button.aria',
    defaultMessage: 'Edit {section} section',
    description: 'Aria label for the edit button',
  },
  'openedx-ai-badges.badge-preview.cancel.button': {
    id: 'openedx-ai-badges.badge-preview.cancel.button',
    defaultMessage: 'Cancel',
    description: 'Label for the cancel button',
  },
  'openedx-ai-badges.badge-preview.skills.target-name': {
    id: 'openedx-ai-badges.badge-preview.skills.target-name',
    defaultMessage: 'Skill Name',
    description: 'Label for skill name',
  },
  'openedx-ai-badges.badge-preview.skills.target-description': {
    id: 'openedx-ai-badges.badge-preview.skills.target-description',
    defaultMessage: 'Description',
    description: 'Label for skill description',
  },
  'openedx-ai-badges.badge-preview.skills.target-type': {
    id: 'openedx-ai-badges.badge-preview.skills.target-type',
    defaultMessage: 'Type',
    description: 'Label for skill type',
  },
  'openedx-ai-badges.badge-preview.badge.criteria': {
    id: 'openedx-ai-badges.badge-preview.badge.criteria',
    defaultMessage: 'Criteria',
    description: 'Label for badge criteria narrative',
  },
  'openedx-ai-badges.badge-preview.edit.error': {
    id: 'openedx-ai-badges.badge-preview.edit.error',
    defaultMessage: 'Invalid JSON',
    description: 'Error message for invalid JSON',
  },
  'openedx-ai-badges.error.generic': {
    id: 'openedx-ai-badges.error.generic',
    defaultMessage: 'Something went wrong. Please try again later.',
    description: 'Generic error message',
  },
  'openedx-ai-badges.badge-form.button.show-form': {
    id: 'openedx-ai-badges.badge-form.button.show-form',
    defaultMessage: 'Regenerate badge',
    description: 'Button that reveals the generation form again so the user can trigger a new (re)generation',
  },
  'openedx-ai-badges.badge-preview.edition-instructions': {
    id: 'openedx-ai-badges.badge-preview.edition-instructions',
    defaultMessage: '<bold>Your badge has been generated successfully!</bold> <br></br> You can now review and edit each section independently using the edit icons. Once you are satisfied, the badge will be saved to the course.',
    description: 'Instructions shown after badge generation',
  },

  // API Status panel
  'openedx-ai-badges.api-status.title': {
    id: 'openedx-ai-badges.api-status.title',
    defaultMessage: 'Service Status',
    description: 'Title for the API status panel',
  },
  'openedx-ai-badges.api-status.online': {
    id: 'openedx-ai-badges.api-status.online',
    defaultMessage: 'Online',
    description: 'Status label when a service is online',
  },
  'openedx-ai-badges.api-status.unavailable': {
    id: 'openedx-ai-badges.api-status.unavailable',
    defaultMessage: 'Unavailable',
    description: 'Status label when a service is unavailable',
  },
  'openedx-ai-badges.api-status.not-configured': {
    id: 'openedx-ai-badges.api-status.not-configured',
    defaultMessage: 'Not configured',
    description: 'Status label when a service is not configured',
  },
  'openedx-ai-badges.api-status.starting': {
    id: 'openedx-ai-badges.api-status.starting',
    defaultMessage: 'Starting',
    description: 'Status label when a service is warming up (e.g. Ollama loading a model)',
  },
  'openedx-ai-badges.api-status.services-offline': {
    id: 'openedx-ai-badges.api-status.services-offline',
    defaultMessage: 'Required services are offline. Badge generation is disabled.',
    description: 'Alert shown when one or more required services are unavailable',
  },
  'openedx-ai-badges.api-status.refresh': {
    id: 'openedx-ai-badges.api-status.refresh',
    defaultMessage: 'Refresh status',
    description: 'Tooltip / aria-label for the refresh button in the API status panel',
  },
  'openedx-ai-badges.api-status.service.badge-api': {
    id: 'openedx-ai-badges.api-status.service.badge-api',
    defaultMessage: 'Badge Generation API',
    description: 'Display name for the badge generation API service',
  },
  'openedx-ai-badges.api-status.service.ollama': {
    id: 'openedx-ai-badges.api-status.service.ollama',
    defaultMessage: 'Ollama Model',
    description: 'Display name for the Ollama model service',
  },
  'openedx-ai-badges.api-status.service.image-api': {
    id: 'openedx-ai-badges.api-status.service.image-api',
    defaultMessage: 'Image Generation API',
    description: 'Display name for the image generation API service',
  },
  'openedx-ai-badges.badge-preview.image.title': {
    id: 'openedx-ai-badges.badge-preview.image.title',
    defaultMessage: 'Badge Image',
    description: 'Title for the badge image section in the preview',
  },
  'openedx-ai-badges.badge-preview.image.no-image': {
    id: 'openedx-ai-badges.badge-preview.image.no-image',
    defaultMessage: 'No image generated yet.',
    description: 'Message shown when no badge image has been generated',
  },
  'openedx-ai-badges.badge-preview.image.button.generate': {
    id: 'openedx-ai-badges.badge-preview.image.button.generate',
    defaultMessage: 'Generate Image',
    description: 'Button to generate a badge image',
  },
  // Planned for future PR:
  // 'openedx-ai-badges.api-status.service.laiser-api': {
  //   id: 'openedx-ai-badges.api-status.service.laiser-api',
  //   defaultMessage: 'LAiSER API',
  //   description: 'Display name for the LAiSER skill extraction service',
  // },
});

export default messages;
