import data from '../data/products.json';

export type Product = {
  model: string;
  category: string;
  name: string;
  dimensions: string;
  widthSeries: number | null;
  price: number | null;
  priceNote: string | null;
  useCase: string;
  image: string;
  flags: string[];
};

export type Category = {
  slug: string;
  name: string;
  nav: string;
  sort: number;
  intro: string;
  hero: string;
};

export const categories: Category[] = [...data.categories].sort((a, b) => a.sort - b.sort);
export const products: Product[] = data.products as Product[];

export function productsIn(slug: string): Product[] {
  return products.filter((p) => p.category === slug);
}

export function category(slug: string): Category {
  const c = categories.find((x) => x.slug === slug);
  if (!c) throw new Error(`Unknown category ${slug}`);
  return c;
}

// Starting price for a category tile. Leg sets are add-ons, not sections, so they
// don't count toward an expansion "from" price.
export function minPrice(slug: string): number | null {
  const prices = productsIn(slug)
    .filter((p) => p.price != null && !/leg set/i.test(p.dimensions))
    .map((p) => p.price as number);
  return prices.length ? Math.min(...prices) : null;
}

export function money(n: number): string {
  if (n < 100 || !Number.isInteger(n)) {
    return '$' + n.toFixed(2);
  }
  return '$' + n.toLocaleString('en-US');
}

export function priceLabel(p: Product): string {
  if (p.priceNote) return p.priceNote;
  if (p.price == null) return 'Call for pricing';
  return money(p.price);
}

// Rough footprint used for the SIZE sort: square feet for kits, square inches
// scaled down for sections, inches for beams and legs.
export function sizeKey(p: Product): number {
  const feet = [...p.dimensions.matchAll(/(\d+)'/g)].map((m) => Number(m[1]));
  if (feet.length >= 3) return feet[0] * feet[1] + feet[2] * feet[0];
  if (feet.length === 2) return feet[0] * feet[1];
  const inches = [...p.dimensions.matchAll(/(\d+)"/g)].map((m) => Number(m[1]));
  if (inches.length >= 2) return (inches[0] * inches[1]) / 144;
  if (inches.length === 1) return inches[0] / 12;
  return p.price ?? 0;
}

export function slugify(model: string): string {
  return model.toLowerCase().replace(/[^a-z0-9]+/g, '-');
}

export function altFor(p: Product): string {
  const kind = ['parts', 'accessories'].includes(p.category) ? 'benchwork part' : 'benchwork kit';
  return `Mianne ${p.model} ${kind}, ${p.dimensions}`;
}

export const PHONE = '508.226.1600';
export const PHONE_TEL = '+15082261600';
export const FAX = '508.226.1666';
export const EMAIL = 'miannebenchwork@gmail.com';
export const YOUTUBE_CHANNEL = 'https://www.youtube.com/channel/UCAE0FFekEmVJkfCfwlrkdSw';
