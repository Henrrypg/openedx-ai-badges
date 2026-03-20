import {
  useState, useCallback, useEffect, useRef,
} from 'react';
import { services } from '@openedx/openedx-ai-extensions-ui';
import { ApiService, ApiStatusResult } from '../types/badges';

const POLL_INTERVAL_MS = 60_000;

interface UseApiStatusReturn {
  services: Record<string, ApiService> | null;
  isLoading: boolean;
  /** True when no required service reports status 'unavailable'. */
  isServicesReady: boolean;
  refresh: () => void;
}

/**
 * Polls `get_api_status` on mount and every 60 seconds.
 *
 * When `enabled` is false the hook is a no-op and always reports ready,
 * so the base BadgeOrchestrator profile incurs zero overhead.
 */
export const useApiStatus = (
  contextData: ReturnType<typeof services.prepareContextData>,
  enabled: boolean,
): UseApiStatusReturn => {
  const [serviceMap, setServiceMap] = useState<Record<string, ApiService> | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const isMountedRef = useRef(true);

  const clearScheduled = useCallback(() => {
    if (timeoutRef.current !== null) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
  }, []);

  const check = useCallback(async () => {
    if (!isMountedRef.current) { return; }
    setIsLoading(true);
    try {
      const result = await services.callWorkflowService({
        payload: { action: 'get_api_status', userInput: {} },
        context: contextData,
      }) as ApiStatusResult;
      if (isMountedRef.current) {
        setServiceMap(result.services ?? null);
      }
    } catch {
      // leave previous state intact on transient error
    } finally {
      if (isMountedRef.current) {
        setIsLoading(false);
        // schedule next check
        timeoutRef.current = setTimeout(() => { check(); }, POLL_INTERVAL_MS);
      }
    }
  }, [contextData]);

  const refresh = useCallback(() => {
    clearScheduled();
    check();
  }, [clearScheduled, check]);

  useEffect(() => {
    if (!enabled) { return undefined; }
    isMountedRef.current = true;
    check();
    return () => {
      isMountedRef.current = false;
      clearScheduled();
    };
  }, [enabled, check, clearScheduled]);

  if (!enabled) {
    return {
      services: null,
      isLoading: false,
      isServicesReady: true,
      refresh: () => {},
    };
  }

  const isServicesReady = serviceMap === null
    || !Object.values(serviceMap).some((s) => s.required && s.status === 'unavailable');

  return {
    services: serviceMap,
    isLoading,
    isServicesReady,
    refresh,
  };
};
