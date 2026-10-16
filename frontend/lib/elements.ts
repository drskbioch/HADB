import theme from '../theme.json';

export const CORE_ELEMENTS = ['Ni', 'Mn', 'Zn', 'Co'] as const;
export const SIDEBAR_ELEMENTS = ['Ni', 'Mn', 'Zn', 'Co', 'Cd', 'Se'] as const;
export const FAMILIES = ['Phyllanthaceae', 'Cunoniaceae', 'Sapotaceae', 'Salicaceae', 'Proteaceae', 'Myrtaceae', 'Euphorbiaceae'] as const;
export const TIERS = ['T1', 'T2', 'T3'] as const;

export function elementColor(e: string): string {
  const m = theme.elements as Record<string, string>;
  return m[e] ?? m.other;
}

export const TIER_TEXT: Record<string, string> = {
  T1: 'T1: taxon-level measurement tested against a threshold (the source class is hyperaccumulator)',
  T2: 'T2: literature label or compiled list (no concentration basis)',
  T3: 'T3: element outside Ni, Mn, Zn, Co, Cd, Se, or no concentration basis',
};
export const SCOPES = ['hyperaccumulation', 'phytoremediation', 'unknown'] as const;
