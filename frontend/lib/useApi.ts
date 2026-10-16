'use client';
import { useEffect, useState } from 'react';
import { api, Params } from './api';

export type State<T> = { data: T | null; error: string | null; loading: boolean };

export function useApi<T>(path: string, params?: Params): State<T> {
  const [state, setState] = useState<State<T>>({ data: null, error: null, loading: true });
  const key = JSON.stringify([path, params]);
  useEffect(() => {
    const ctl = new AbortController();
    setState((s) => ({ ...s, loading: true, error: null }));
    api<T>(path, params, ctl.signal)
      .then((data) => setState({ data, error: null, loading: false }))
      .catch((e: Error) => { if (e.name !== 'AbortError') setState({ data: null, error: e.message === 'Failed to fetch' ? 'Please reload the page.' : e.message, loading: false }); });
    return () => ctl.abort();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [key]);
  return state;
}
