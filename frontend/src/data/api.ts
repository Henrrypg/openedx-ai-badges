import { services } from '@openedx/openedx-ai-extensions-ui';
import { ProfileConfig } from '../types/badges';

export const getProfileConfig = async (
  contextData: ReturnType<typeof services.prepareContextData>,
): Promise<ProfileConfig | null> => {
  const config = await services.fetchConfiguration({
    contextData,
    configEndpoint: services.getDefaultEndpoint('profile'),
  });
  return config as ProfileConfig | null;
};
