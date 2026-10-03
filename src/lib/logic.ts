/**
 * Tiny propositional-logic toolkit shared by the interactive components
 * (LogicPlayground, EquivalenceChecker). Accepts ASCII (->, <->, ~, &, |, ^) and logic symbols.
 * Precedence: not > and > xor > or > implies (right-assoc) > iff.
 */
export type Node =
  | { t: 'var'; name: string }
  | { t: 'const'; v: boolean }
  | { t: 'not'; a: Node }
  | { t: 'bin'; op: 'and' | 'or' | 'xor' | 'imp' | 'iff'; a: Node; b: Node };

export const OPS: [RegExp, string][] = [
  [/^(<->|<=>|↔|⇔|iff\b)/, 'iff'],
  [/^(->|=>|→|⇒|implies\b)/, 'imp'],
  [/^(&&|&|∧|and\b)/, 'and'],
  [/^(\|\||\||∨|or\b)/, 'or'],
  [/^(\^|⊕|xor\b)/, 'xor'],
  [/^(~|!|¬|not\b)/, 'not'],
  [/^\(/, '('],
  [/^\)/, ')'],
];

export function tokenize(src: string): string[] {
  const out: string[] = [];
  let s = src.trim();
  while (s.length) {
    if (/^\s/.test(s)) { s = s.trimStart(); continue; }
    let hit = false;
    for (const [re, name] of OPS) {
      const m = s.match(re);
      if (m) { out.push(name); s = s.slice(m[0].length); hit = true; break; }
    }
    if (hit) continue;
    const c = s.match(/^(true|false|T|F|1|0)\b/);
    if (c) { out.push(/^(true|T|1)$/.test(c[1]) ? '#1' : '#0'); s = s.slice(c[0].length); continue; }
    const v = s.match(/^[a-z][a-z0-9_]*/);
    if (v) { out.push('$' + v[0]); s = s.slice(v[0].length); continue; }
    throw new Error(`Unexpected “${s[0]}”`);
  }
  return out;
}

// precedence: not > and > xor > or > imp (right-assoc) > iff
export function parse(tokens: string[]): Node {
  let i = 0;
  const peek = () => tokens[i];
  const eat = (x: string) => { if (tokens[i] !== x) throw new Error(`Expected “${x === ')' ? ')' : x}”`); i++; };
  const iff = (): Node => { let a = imp(); while (peek() === 'iff') { i++; a = { t: 'bin', op: 'iff', a, b: imp() }; } return a; };
  const imp = (): Node => { const a = or(); if (peek() === 'imp') { i++; return { t: 'bin', op: 'imp', a, b: imp() }; } return a; };
  const or = (): Node => { let a = xor(); while (peek() === 'or') { i++; a = { t: 'bin', op: 'or', a, b: xor() }; } return a; };
  const xor = (): Node => { let a = and(); while (peek() === 'xor') { i++; a = { t: 'bin', op: 'xor', a, b: and() }; } return a; };
  const and = (): Node => { let a = not(); while (peek() === 'and') { i++; a = { t: 'bin', op: 'and', a, b: not() }; } return a; };
  const not = (): Node => { if (peek() === 'not') { i++; return { t: 'not', a: not() }; } return atom(); };
  const atom = (): Node => {
    const k = peek();
    if (k === undefined) throw new Error('Formula ends too early');
    if (k === '(') { i++; const n = iff(); eat(')'); return n; }
    if (k.startsWith('$')) { i++; return { t: 'var', name: k.slice(1) }; }
    if (k.startsWith('#')) { i++; return { t: 'const', v: k === '#1' }; }
    throw new Error(`Unexpected operator`);
  };
  if (!tokens.length) throw new Error('Type a formula');
  const n = iff();
  if (i < tokens.length) throw new Error(tokens[i] === ')' ? 'Unbalanced “)”' : 'Missing operator between terms');
  return n;
}

export const vars = (n: Node, acc = new Set<string>()): Set<string> => {
  if (n.t === 'var') acc.add(n.name);
  else if (n.t === 'not') vars(n.a, acc);
  else if (n.t === 'bin') { vars(n.a, acc); vars(n.b, acc); }
  return acc;
};

export const ev = (n: Node, env: Record<string, boolean>): boolean => {
  switch (n.t) {
    case 'var': return env[n.name];
    case 'const': return n.v;
    case 'not': return !ev(n.a, env);
    case 'bin': {
      const a = ev(n.a, env), b = ev(n.b, env);
      return n.op === 'and' ? a && b : n.op === 'or' ? a || b : n.op === 'xor' ? a !== b : n.op === 'imp' ? !a || b : a === b;
    }
  }
};

export const SYM = { and: '∧', or: '∨', xor: '⊕', imp: '→', iff: '↔' } as const;
export const show = (n: Node, top = true): string => {
  if (n.t === 'var') return n.name;
  if (n.t === 'const') return n.v ? 'T' : 'F';
  if (n.t === 'not') return '¬' + show(n.a, false);
  const s = `${show(n.a, false)} ${SYM[n.op]} ${show(n.b, false)}`;
  return top ? s : `(${s})`;
};
export const py = (n: Node): string => {
  if (n.t === 'var') return n.name;
  if (n.t === 'const') return n.v ? 'True' : 'False';
  if (n.t === 'not') return `not ${py(n.a)}`;
  const a = py(n.a), b = py(n.b);
  switch (n.op) {
    case 'and': return `(${a} and ${b})`;
    case 'or': return `(${a} or ${b})`;
    case 'xor': return `(${a} != ${b})`;
    case 'imp': return `((not ${a}) or ${b})`;
    case 'iff': return `(${a} == ${b})`;
  }
};

// sub-formulas for intermediate columns (binary nodes only, innermost first, max 4)
export const subs = (n: Node, acc: Node[] = []): Node[] => {
  if (n.t === 'not') subs(n.a, acc);
  if (n.t === 'bin') { subs(n.a, acc); subs(n.b, acc); acc.push(n); }
  return acc;
};

/** All assignments of the variables, True first, last variable fastest. */
export function rowsOf(vs: string[]): Record<string, boolean>[] {
  const out: Record<string, boolean>[] = [];
  for (let r = 0; r < 1 << vs.length; r++) {
    const env: Record<string, boolean> = {};
    vs.forEach((v, k) => (env[v] = !((r >> (vs.length - 1 - k)) & 1)));
    out.push(env);
  }
  return out;
}

/** Parse a formula string into an AST (throws Error with a readable message). */
export const compile = (src: string): Node => parse(tokenize(src));
