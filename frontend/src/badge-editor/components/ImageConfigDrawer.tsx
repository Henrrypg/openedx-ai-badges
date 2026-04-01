import { useIntl } from '@edx/frontend-platform/i18n';
import { Button } from '@openedx/paragon';
import { ImageConfiguration } from '../../types/badges';
import messages from '../messages';

const MODES = [
  { value: 'icon_based', msgKey: 'openedx.ai.badges.editor.imageConfig.mode.icon' },
  { value: 'text_overlay', msgKey: 'openedx.ai.badges.editor.imageConfig.mode.text' },
] as const;

const RIBBON_OPTIONS = [
  { value: '', msgKey: 'openedx.ai.badges.editor.imageConfig.ribbon.auto' },
  { value: 'ribbon', msgKey: 'openedx.ai.badges.editor.imageConfig.ribbon.ribbon' },
  { value: 'ribbon_folded', msgKey: 'openedx.ai.badges.editor.imageConfig.ribbon.ribbon_folded' },
  { value: 'none', msgKey: 'openedx.ai.badges.editor.imageConfig.ribbon.none' },
] as const;

const SHAPES = [
  { value: '', msgKey: 'openedx.ai.badges.editor.imageConfig.shape.auto' },
  { value: 'hexagon', msgKey: 'openedx.ai.badges.editor.imageConfig.shape.hexagon' },
  { value: 'circle', msgKey: 'openedx.ai.badges.editor.imageConfig.shape.circle' },
  { value: 'rounded_rect', msgKey: 'openedx.ai.badges.editor.imageConfig.shape.rounded_rect' },
] as const;

export interface ImageConfigState {
  mode: 'icon_based' | 'text_overlay';
  shape: string;
  primaryColorEnabled: boolean;
  primaryColor: string;
  secondaryColorEnabled: boolean;
  secondaryColor: string;
  borderWidth: number;
  borderColorEnabled: boolean;
  borderColor: string;
  ribbonType: string;
}

export const DEFAULT_STATE: ImageConfigState = {
  mode: 'icon_based',
  shape: '',
  primaryColorEnabled: false,
  primaryColor: '#4b9fdc',
  secondaryColorEnabled: false,
  secondaryColor: '#2b6db3',
  borderWidth: 0,
  borderColorEnabled: false,
  borderColor: '#000000',
  ribbonType: '',
};

export const buildImageConfig = (state: ImageConfigState): ImageConfiguration => {
  const config: ImageConfiguration = {};
  if (state.shape) { config.shape = state.shape; }
  if (state.primaryColorEnabled) { config.primary_color = state.primaryColor; }
  if (state.secondaryColorEnabled) { config.secondary_color = state.secondaryColor; }
  if (state.borderWidth > 0) {
    config.border_width = state.borderWidth;
    if (state.borderColorEnabled) { config.border_color = state.borderColor; }
  }
  if (state.mode === 'text_overlay' && state.ribbonType) {
    config.ribbon_type = state.ribbonType;
  }
  return config;
};

interface ImageConfigDrawerProps {
  isOpen: boolean;
  state: ImageConfigState;
  onChange: (state: ImageConfigState) => void;
}

const ImageConfigDrawer = ({ isOpen, state, onChange }: ImageConfigDrawerProps) => {
  const intl = useIntl();
  const set = (patch: Partial<ImageConfigState>) => onChange({ ...state, ...patch });

  return (
    <div className={`image-config-panel ${isOpen ? 'image-config-panel--open' : ''}`}>
      <div className="image-config-panel__inner">

        {/* Mode */}
        <div className="image-config-panel__row">
          <span className="image-config-panel__label">
            {intl.formatMessage(messages['openedx.ai.badges.editor.imageConfig.mode.label'])}
          </span>
          <div className="d-flex gap-1">
            {MODES.map(({ value, msgKey }) => (
              <Button
                key={value}
                size="sm"
                variant={state.mode === value ? 'primary' : 'outline-primary'}
                onClick={() => set({ mode: value })}
                className="image-config-panel__shape-btn"
              >
                {intl.formatMessage(messages[msgKey])}
              </Button>
            ))}
          </div>
        </div>

        {/* Shape */}
        <div className="image-config-panel__row">
          <span className="image-config-panel__label">
            {intl.formatMessage(messages['openedx.ai.badges.editor.imageConfig.shape.label'])}
          </span>
          <div className="d-flex gap-1 flex-wrap">
            {SHAPES.map(({ value, msgKey }) => (
              <Button
                key={value || 'auto'}
                size="sm"
                variant={state.shape === value ? 'primary' : 'outline-primary'}
                onClick={() => set({ shape: value })}
                className="image-config-panel__shape-btn"
              >
                {intl.formatMessage(messages[msgKey])}
              </Button>
            ))}
          </div>
        </div>

        {/* Primary color */}
        <div className="image-config-panel__row">
          <label className="image-config-panel__color-label" htmlFor="img-cfg-primary">
            <input
              type="checkbox"
              checked={state.primaryColorEnabled}
              onChange={(e) => set({ primaryColorEnabled: e.target.checked })}
            />
            <span className="image-config-panel__label">
              {intl.formatMessage(messages['openedx.ai.badges.editor.imageConfig.primaryColor.label'])}
            </span>
          </label>
          {state.primaryColorEnabled && (
            <input
              id="img-cfg-primary"
              type="color"
              value={state.primaryColor}
              onChange={(e) => set({ primaryColor: e.target.value })}
              className="image-config-panel__color-swatch"
            />
          )}
        </div>

        {/* Secondary color */}
        <div className="image-config-panel__row">
          <label className="image-config-panel__color-label" htmlFor="img-cfg-secondary">
            <input
              type="checkbox"
              checked={state.secondaryColorEnabled}
              onChange={(e) => set({ secondaryColorEnabled: e.target.checked })}
            />
            <span className="image-config-panel__label">
              {intl.formatMessage(messages['openedx.ai.badges.editor.imageConfig.secondaryColor.label'])}
            </span>
          </label>
          {state.secondaryColorEnabled && (
            <input
              id="img-cfg-secondary"
              type="color"
              value={state.secondaryColor}
              onChange={(e) => set({ secondaryColor: e.target.value })}
              className="image-config-panel__color-swatch"
            />
          )}
        </div>

        {/* Border width */}
        <div className="image-config-panel__row">
          <span className="image-config-panel__label">
            {intl.formatMessage(messages['openedx.ai.badges.editor.imageConfig.border.label'])}
          </span>
          <div className="image-config-panel__slider-row">
            <input
              type="range"
              min={0}
              max={20}
              value={state.borderWidth}
              onChange={(e) => set({ borderWidth: parseInt(e.target.value, 10) })}
              className="image-config-panel__slider"
              aria-label={intl.formatMessage(messages['openedx.ai.badges.editor.imageConfig.borderWidth.label'])}
            />
            <span className="image-config-panel__px">{state.borderWidth}px</span>
          </div>
        </div>

        {/* Border color — only when width > 0 */}
        {state.borderWidth > 0 && (
          <div className="image-config-panel__row image-config-panel__row--indented">
            <label className="image-config-panel__color-label" htmlFor="img-cfg-border">
              <input
                type="checkbox"
                checked={state.borderColorEnabled}
                onChange={(e) => set({ borderColorEnabled: e.target.checked })}
              />
              <span className="image-config-panel__label">
                {intl.formatMessage(messages['openedx.ai.badges.editor.imageConfig.borderColor.label'])}
              </span>
            </label>
            {state.borderColorEnabled && (
              <input
                id="img-cfg-border"
                type="color"
                value={state.borderColor}
                onChange={(e) => set({ borderColor: e.target.value })}
                className="image-config-panel__color-swatch"
              />
            )}
          </div>
        )}

        {/* Ribbon — only available in text mode */}
        {state.mode === 'text_overlay' && (
          <div className="image-config-panel__row">
            <span className="image-config-panel__label">
              {intl.formatMessage(messages['openedx.ai.badges.editor.imageConfig.ribbon.label'])}
            </span>
            <div className="d-flex gap-1 flex-wrap">
              {RIBBON_OPTIONS.map(({ value, msgKey }) => (
                <Button
                  key={value || 'auto'}
                  size="sm"
                  variant={state.ribbonType === value ? 'primary' : 'outline-primary'}
                  onClick={() => set({ ribbonType: value })}
                  className="image-config-panel__shape-btn"
                >
                  {intl.formatMessage(messages[msgKey])}
                </Button>
              ))}
            </div>
          </div>
        )}

        {/* Reset */}
        <div className="image-config-panel__row image-config-panel__row--reset">
          <Button
            variant="tertiary"
            size="sm"
            onClick={() => onChange(DEFAULT_STATE)}
          >
            {intl.formatMessage(messages['openedx.ai.badges.editor.imageConfig.reset'])}
          </Button>
        </div>

      </div>
    </div>
  );
};

export default ImageConfigDrawer;
