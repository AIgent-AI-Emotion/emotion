export type Metrics = Record<string, number | string | boolean>;

export interface KWord {
  id?: string;
  name: string;
  tags: string[];
  attributes?: Record<string, unknown>;
  created_at?: string;
}

export interface Health {
  status: 'ok' | 'degraded' | 'down';
  service: string;
  version: string;
  runtime: string;
}
