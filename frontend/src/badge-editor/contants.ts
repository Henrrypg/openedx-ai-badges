import { FormOptionsMap, BadgeFormData } from '../types/badges';
import messages from './messages';

export const FORM_OPTIONS: FormOptionsMap = {
  style: [
    { value: 'modern', label: messages['openedx.ai.badges.editor.create.style.modern'] },
    { value: 'classic', label: messages['openedx.ai.badges.editor.create.style.classic'] },
    { value: 'minimalist', label: messages['openedx.ai.badges.editor.create.style.minimalist'] },
    { value: 'playful', label: messages['openedx.ai.badges.editor.create.style.playful'] },
  ],
  tone: [
    { value: 'professional', label: messages['openedx.ai.badges.editor.create.tone.professional'] },
    { value: 'friendly', label: messages['openedx.ai.badges.editor.create.tone.friendly'] },
    { value: 'academic', label: messages['openedx.ai.badges.editor.create.tone.academic'] },
    { value: 'creative', label: messages['openedx.ai.badges.editor.create.tone.creative'] },
  ],
  level: [
    { value: 'beginner', label: messages['openedx.ai.badges.editor.create.level.beginner'] },
    { value: 'intermediate', label: messages['openedx.ai.badges.editor.create.level.intermediate'] },
    { value: 'advanced', label: messages['openedx.ai.badges.editor.create.level.advanced'] },
    { value: 'expert', label: messages['openedx.ai.badges.editor.create.level.expert'] },
  ],
  criterion: [
    { value: 'completion', label: messages['openedx.ai.badges.editor.create.criterion.completion'] },
    { value: 'mastery', label: messages['openedx.ai.badges.editor.create.criterion.mastery'] },
    { value: 'participation', label: messages['openedx.ai.badges.editor.create.criterion.participation'] },
    { value: 'excellence', label: messages['openedx.ai.badges.editor.create.criterion.excellence'] },
  ],
};

export const DEFAULT_FORM_DATA: BadgeFormData = {
  style: 'modern',
  tone: 'professional',
  level: 'intermediate',
  criterion: 'completion',
  skillsEnabled: true,
  additionalInstructions: '',
};
