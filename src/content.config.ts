import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const link = z.object({ title: z.string(), url: z.string(), note: z.string().optional() });

const weeks = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './content/weeks' }),
  schema: z.object({
    week: z.number().int().min(1),
    title: z.string(),
    description: z.string(),
    module: z.string(),
    exam: z.boolean().default(false),
    // draft: outline only | ready: notes published
    status: z.enum(['draft', 'ready']).default('draft'),
    changeNote: z.string().default(''),
    reading: z.string().default(''),          // e.g. "Rosen 1.1–1.2"
    objectives: z.array(z.string()).default([]),
    // the "wow" moment of the week: one striking real-world connection
    wow: z.object({ title: z.string(), text: z.string() }).optional(),
    industry: z.array(z.object({ t: z.string(), d: z.string() })).default([]),
    lab: z.string().optional(),               // lab slug, e.g. "lab-01"
    slides: z.array(z.object({ title: z.string(), file: z.string() })).default([]),
    resources: z.array(link).default([]),
    tags: z.array(z.string()).default([]),
  }),
});

const labs = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './content/labs' }),
  schema: z.object({
    lab: z.number().int().min(0),
    week: z.number().int(),
    title: z.string(),
    description: z.string(),
    assignment: z.string(),                   // Classroom 50 assignment slug, e.g. "lab01"
    acceptUrl: z.string().default(''),        // Classroom 50 accept link for this assignment (optional)
    // classroom50: accept on classroom50.org | template: students copy a public template into their own account (plan B)
    mode: z.enum(['classroom50', 'template']).default('classroom50'),
    status: z.enum(['draft', 'open', 'closed']).default('draft'),
    due: z.string().default(''),              // YYYY-MM-DD HH:mm, local time
    duration: z.string().default('75 min'),
    points: z.number().default(10),
    files: z.array(z.string()).default([]),
    topics: z.array(z.string()).default([]),
    notebook: z.object({ file: z.string(), title: z.string().optional() }).optional(),
  }),
});

const announcements = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './content/announcements' }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    pinned: z.boolean().default(false),
    kind: z.enum(['info', 'important', 'exam', 'lab']).default('info'),
  }),
});

const guides = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './content/guides' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    order: z.number().default(99),
  }),
});

export const collections = { weeks, labs, announcements, guides };
