import { useQuery } from '@tanstack/react-query';
import { services } from '@openedx/openedx-ai-extensions-ui';
import { GeneratedBadge } from '../../types/badges';
import { getBadges } from './api';
import { pluginId } from '../../contants';

export const queryKey = {
  all: [pluginId, 'badges-list'],
  list: (contextData) => [...queryKey.all, contextData],
};

export const useListBadges = (
  contextData: ReturnType<typeof services.prepareContextData>,
) => {
  const query = useQuery<GeneratedBadge[]>({
    queryKey: queryKey.list(contextData),
    queryFn: () => getBadges(contextData),
  });
  return {
    data: query.data,
    isLoading: query.isLoading,
    error: query.error instanceof Error ? query.error.message : null,
  };
};
