import data from '../data/blog.json';

export type Post = {
  title: string;
  slug: string;
  date: string;
  description: string;
  thumbnail?: string;
  body: string;
};

export const posts: Post[] = ((data.posts ?? []) as Post[])
  .filter((p) => p && p.slug && p.title)
  .sort((a, b) => (a.date < b.date ? 1 : -1));

// Articles queued for the blog launch (content.md). Shown until real posts exist.
export const upcoming = [
  'What Size Train Layout Fits Your Basement? A Room-by-Room Guide',
  'HO vs O Gauge: How Much Bench Do You Really Need?',
  'Benchwork Without Power Tools: Why Cam Locks Beat Carpentry',
  'Planning an Around the Room Layout: Depth, Reach, and Aisles',
  'Moving a Model Railroad: How to Take Your Layout With You',
  'Club and Hobby Shop Benchwork: Displays That Break Down and Travel',
];

export function prettyDate(d: string): string {
  const dt = new Date(d + 'T12:00:00');
  return dt.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
}
