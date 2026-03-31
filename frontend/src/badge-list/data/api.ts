import { services } from '@openedx/openedx-ai-extensions-ui';
import { GeneratedBadge } from '../../types/badges';

interface GetBadgesResult {
  response: GeneratedBadge[];
  status: 'completed' | 'empty';
}

export const getBadges = async (
  contextData: ReturnType<typeof services.prepareContextData>,
): Promise<GeneratedBadge[]> => {
  const result = await services.callWorkflowService({
    payload: { action: 'get_badges', userInput: {} },
    context: contextData,
  }) as GetBadgesResult;
  return result.response ?? [];
};
