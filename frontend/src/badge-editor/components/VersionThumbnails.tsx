import { useIntl } from '@edx/frontend-platform/i18n';
import { BadgeImageResult } from '../../types/badges';
import messages from '../messages';

interface VersionThumbnailsProps {
  images: BadgeImageResult[];
  selectedImage: BadgeImageResult | null;
  onSelect: (image: BadgeImageResult) => void;
}

const VersionThumbnails = ({ images, selectedImage, onSelect }: VersionThumbnailsProps) => {
  const intl = useIntl();

  const toSrc = (image: BadgeImageResult) => (
    image.base64.startsWith('data:') ? image.base64 : `data:image/png;base64,${image.base64}`
  );

  if (images.length === 0) {
    return null;
  }

  return (
    <div className="d-flex gap-2 flex-wrap badge-preview__versions">
      {images.map((image, idx) => {
        const isActive = selectedImage?.base64 === image.base64;
        return (
          <button
            key={image.base64}
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              const newValue = isActive ? null : image;
              if (newValue) {
                onSelect(newValue);
              }
            }}
            className={`badge-preview__version-thumb rounded p-0 border-0 bg-transparent${isActive ? ' badge-preview__version-thumb--active' : ''}`}
            aria-pressed={isActive}
            aria-label={intl.formatMessage(messages['openedx.ai.badges.editor.preview.selectVersion'], { index: idx + 1 })}
          >
            <img src={toSrc(image)} alt="" className="img-fluid rounded" />
          </button>
        );
      })}
    </div>
  );
};

export default VersionThumbnails;
