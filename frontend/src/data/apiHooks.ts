import { useQuery } from '@tanstack/react-query';
import { services } from '@openedx/openedx-ai-extensions-ui';
import { ProfileConfig } from '../types/badges';
import { fetchProfileConfig } from './api';
import { pluginId } from '../contants';

const queryKey = {
  all: [pluginId, 'profile'],
  config: (contextData) => [...queryKey.all, contextData],
};

export const useProfileConfig = (
  contextData: ReturnType<typeof services.prepareContextData>,
) => useQuery<ProfileConfig | null>({
  queryKey: queryKey.config(contextData),
  queryFn: () => fetchProfileConfig(contextData),
});
