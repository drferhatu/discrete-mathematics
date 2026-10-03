import course from '@content/data/course.json';
import modules from '@content/data/modules.json';
import schedule from '@content/data/schedule.json';
import { getCollection, type CollectionEntry } from 'astro:content';

export { course, modules, schedule };

export type Module = (typeof modules)[number];
export type Week = CollectionEntry<'weeks'>;
export type Lab = CollectionEntry<'labs'>;
export type ScheduleRow = (typeof schedule.weeks)[number];

export const REPO = 'drferhatu/discrete-mathematics';

/** base-aware link: href('/weeks') → '/discrete-mathematics/weeks' */
export function href(path: string): string {
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  if (path === '/') return base + '/';
  return base + (path.startsWith('/') ? path : '/' + path);
}

export const pad = (n: number) => String(n).padStart(2, '0');
export const weekSlug = (n: number) => `week-${pad(n)}`;
export const weekHref = (n: number) => href(`/weeks/${weekSlug(n)}`);
export const labHref = (slug: string) => href(`/labs/${slug}`);

export function moduleOf(id: string): Module {
  const m = modules.find((x) => x.id === id);
  if (!m) throw new Error(`Unknown module: ${id}`);
  return m;
}

export function scheduleOf(n: number): ScheduleRow | undefined {
  return schedule.weeks.find((r) => r.week === n);
}

export async function getWeeksSorted(): Promise<Week[]> {
  return (await getCollection('weeks')).sort((a, b) => a.data.week - b.data.week);
}

export async function getLabsSorted(): Promise<Lab[]> {
  return (await getCollection('labs')).sort((a, b) => a.data.lab - b.data.lab);
}

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const MONTHS_LONG = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

export function formatDate(iso: string | undefined, long = false): string {
  if (!iso) return '';
  const [y, m, d] = iso.slice(0, 10).split('-').map(Number);
  if (!y || !m || !d) return '';
  return long ? `${MONTHS_LONG[m - 1]} ${d}, ${y}` : `${MONTHS[m - 1]} ${d}`;
}

export function formatDateObj(d: Date): string {
  return `${MONTHS_LONG[d.getMonth()]} ${d.getDate()}, ${d.getFullYear()}`;
}

export const STATUS_LABEL: Record<string, string> = {
  normal: '',
  holiday: 'Holiday, no class',
  postponed: 'Postponed',
  exam: 'Exam week',
};

/**
 * Where a student starts a lab: the Classroom 50 accept page (classroom50 mode, derived from the
 * assignment slug unless `acceptUrl` overrides it) or the template's "create a copy" form (template mode).
 */
export function labStartUrl(lab: Lab): string {
  const c = course.classroom;
  if (lab.data.mode === 'template') return `https://github.com/${c.org}/${c.prefix}-${lab.data.assignment}-template/generate`;
  return lab.data.acceptUrl || `${c.web}/${c.org}/${c.slug}/assignments/${lab.data.assignment}/accept`;
}

/** Classroom 50 accept command for a lab assignment */
export function acceptCmd(assignment: string) {
  return `gh student accept ${course.classroom.org} ${course.classroom.slug} ${assignment}`;
}
export function repoName(assignment: string) {
  return `${course.classroom.slug}-${assignment}-USERNAME`.toLowerCase().replace('username', 'USERNAME');
}

export const moduleColorVar = (m: Module) => `var(--mod-${m.color})`;

/** Lab deadline: the lab's own `due`, otherwise Friday 23:59 of its week ("YYYY-MM-DD HH:mm"). */
export function labDue(lab: Lab): string {
  if (lab.data.due) return lab.data.due;
  const monday = scheduleOf(lab.data.week)?.date;
  if (!monday) return '';
  const d = new Date(monday + 'T12:00:00Z');
  d.setUTCDate(d.getUTCDate() + 4);
  return `${d.toISOString().slice(0, 10)} 23:59`;
}

const WEEKDAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
/** "Fri, Oct 2 · 23:59" */
export function formatDue(due: string): string {
  if (!due) return '';
  const d = new Date(due.slice(0, 10) + 'T12:00:00Z');
  return `${WEEKDAYS[d.getUTCDay()]}, ${formatDate(due)} · ${due.slice(11) || '23:59'}`;
}

/** The week students should look at: today's class, else the next upcoming one (evaluated at build time). */
export function currentWeek(today = new Date()): number {
  const iso = today.toISOString().slice(0, 10);
  const next = schedule.weeks.find((r) => r.date && r.date >= iso);
  return next ? next.week : schedule.weeks[schedule.weeks.length - 1].week;
}
