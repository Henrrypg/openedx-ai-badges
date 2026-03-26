import { useMemo } from 'react';
import { useIntl } from '@edx/frontend-platform/i18n';
import {
  Button, Container, DataTable, CardView, TextFilter, Spinner,
} from '@openedx/paragon';
import { Add } from '@openedx/paragon/icons';
import { services } from '@openedx/openedx-ai-extensions-ui';
import { useListBadges } from './data/apiHooks';
import EmptyStateView from './EmptyStateView';
import BadgeCard from './BadgeCard';
import messages from './messages';
import { GeneratedBadge } from '../types/badges';

interface GalleryViewProps {
  contextData: ReturnType<typeof services.prepareContextData>;
  onCreateNew: () => void;
  onEdit: (badge: GeneratedBadge) => void;
}

const CreateBadgeAction = ({ onCreateNew }: { onCreateNew: () => void }) => {
  const intl = useIntl();
  return (
    <Button variant="primary" iconBefore={Add} onClick={onCreateNew}>
      {intl.formatMessage(messages['openedx.ai.badges.button.create'])}
    </Button>
  );
};

const GalleryView = ({ contextData, onCreateNew, onEdit }: GalleryViewProps) => {
  const intl = useIntl();
  const { data: badges = [], isLoading } = useListBadges(contextData);

  const columns = useMemo(() => [
    {
      id: 'name',
      Header: intl.formatMessage(messages['openedx.ai.badges.gallery.column.name']),
      accessor: (row: GeneratedBadge) => row.generatedResponse?.credentialSubject?.achievement?.name ?? '',
    },
  ], [intl]);

  if (isLoading) {
    return (
      <Container className="d-flex justify-content-center align-items-center py-5">
        <Spinner animation="border" screenReaderText={intl.formatMessage(messages['openedx.ai.badges.gallery.loading'])} />
      </Container>
    );
  }

  if (badges.length === 0) {
    return <EmptyStateView onCreateNew={onCreateNew} />;
  }

  return (
    <Container className="py-4">
      <h2 className="mb-4">{intl.formatMessage(messages['openedx.ai.badges.gallery.title'])}</h2>
      <DataTable
        isFilterable
        defaultColumnValues={{ Filter: TextFilter }}
        itemCount={badges.length}
        data={badges}
        columns={columns}
        tableActions={[
          <CreateBadgeAction onCreateNew={onCreateNew} />,
        ]}
      >
        <DataTable.TableControlBar />
        <CardView
          CardComponent={BadgeCard}
        />
        <DataTable.EmptyTable
          content={intl.formatMessage(messages['openedx.ai.badges.gallery.no.results'])}
        />
        <DataTable.TableFooter />
      </DataTable>
    </Container>
  );
};

export default GalleryView;
