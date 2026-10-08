// Page copy for each catalog category (content.md + seo.md). Product data stays in products.json.
export type CategoryPage = {
  h1: string;
  intro: string;
  title: string;
  description: string;
  hero: string; // base name in images/, e.g. hero-starter
  heroAlt: string;
  tile: string; // ALL CAPS tile label
  tileSub: string;
  widthFilter: boolean;
  seriesSwitch?: boolean;
};

export const categoryPages: Record<string, CategoryPage> = {
  'starter-kits': {
    h1: 'Starter Kits',
    intro:
      "One rectangular table, everything in the box, up in about an hour. This is the classic first Mianne: the footprint of a sheet of plywood without the plywood, the sawing, or the swearing. Twenty-two sizes from a 2x6 shelf to an 8x8 island.",
    title: 'Starter Kit Train Tables, 2x6 to 8x8 | Mianne Benchwork',
    description:
      'Rectangular model train tables that assemble in about an hour. 22 sizes with prices listed. Solid hardwood, no power tools.',
    hero: 'hero-starter',
    heroAlt: 'A Mianne 4x8 starter table with a half-finished HO layout in a tidy garage',
    tile: 'STARTER KITS',
    tileSub: 'Rectangular tables, 2x6 to 8x8',
    widthFilter: false,
  },
  '24-series': {
    h1: '24 Series Classic Layouts',
    intro:
      'Shaped layouts built from 24 inch wide sections: L-shapes, long runs, and around-the-corner plans. The 24 inch width keeps every inch of track within easy reach, which your back will appreciate at hour three of scenery work.',
    title: '24 Series Classic Layout Kits | Mianne Benchwork',
    description:
      'Shaped layout benchwork with 24 inch sections that keep every rail in easy reach. Sizes and prices listed.',
    hero: 'hero-classic',
    heroAlt: 'L-shaped Mianne benchwork along two basement walls with a sceniced layout on top',
    tile: '24 SERIES',
    tileSub: 'Shaped classics, 24" sections',
    widthFilter: false,
    seriesSwitch: true,
  },
  '30-series': {
    h1: '30 Series Classic Layouts',
    intro:
      'The same classic shapes with 30 inch wide sections. The sweet spot for a lot of HO and O gauge plans: enough depth for real scenery, still shallow enough to reach the back rail.',
    title: '30 Series Classic Layout Kits | Mianne Benchwork',
    description:
      'Classic shaped benchwork with 30 inch sections, the HO and O gauge sweet spot. Sizes and prices listed.',
    hero: 'hero-classic',
    heroAlt: 'L-shaped Mianne benchwork along two basement walls with a sceniced layout on top',
    tile: '30 SERIES',
    tileSub: 'Shaped classics, 30" sections',
    widthFilter: false,
    seriesSwitch: true,
  },
  '36-series': {
    h1: '36 Series Classic Layouts',
    intro:
      "Classic shapes with a full 36 inches of depth. Room for broad curves, double mainlines, and mountains worth the name. Best where you can reach from both sides or don't mind a step stool.",
    title: '36 Series Classic Layout Kits | Mianne Benchwork',
    description:
      'Classic shapes with 36 inches of depth for broad curves and big scenery. Sizes and prices listed.',
    hero: 'hero-classic',
    heroAlt: 'L-shaped Mianne benchwork along two basement walls with a sceniced layout on top',
    tile: '36 SERIES',
    tileSub: 'Shaped classics, 36" sections',
    widthFilter: false,
    seriesSwitch: true,
  },
  'around-the-room': {
    h1: 'Around the Room Kits',
    intro:
      'Benchwork that follows your walls so your trains never stop running. Pick your room size, then pick your depth: 24, 30, or 36 inch sections on the long sides. Footprints from 8x12 up to 12x24.',
    title: 'Around the Room Train Layout Kits | Mianne Benchwork',
    description:
      'Continuous-running benchwork that follows your walls. Footprints 8x12 to 12x24 in three depths, prices listed.',
    hero: 'hero-around',
    heroAlt: 'Mianne benchwork running around all four walls of a finished basement',
    tile: 'AROUND THE ROOM',
    tileSub: 'Continuous running, wall to wall',
    widthFilter: true,
  },
  'walk-through': {
    h1: 'Walk-Through Kits',
    intro:
      'All the continuous running of an around-the-room layout with a real opening to walk through. No duck-under, no crawling, no apologizing to your knees. Also available Lift-Gate ready for a motorized section that rises out of your way.',
    title: 'Walk-Through Layout Kits, No Duck-Under | Mianne Benchwork',
    description:
      'Around-the-room benchwork with a real walk-through opening. Lift-Gate ready versions available. Prices listed.',
    hero: 'hero-walkthrough',
    heroAlt: 'U-shaped Mianne walk-through benchwork with an open entry between the two runs',
    tile: 'WALK-THROUGH',
    tileSub: 'No duck-under, walk right in',
    widthFilter: true,
  },
  expansion: {
    h1: 'Expansion Sections',
    intro:
      "The layout you have today doesn't have to be the layout you keep. Straight and corner sections bolt onto any Mianne layout, legs included. Add a leg set and any section stands on its own. Nothing you own becomes obsolete.",
    title: 'Expansion Sections for Mianne Layouts',
    description:
      'Straight and corner sections that grow any Mianne layout, legs included. Nothing you own becomes obsolete.',
    hero: 'hero-expansion',
    heroAlt: 'A new unfinished Mianne section joined to a finished, sceniced layout',
    tile: 'EXPANSION SECTIONS',
    tileSub: "Grow what you've got",
    widthFilter: true,
  },
  parts: {
    h1: 'Parts & Accessories',
    intro:
      "Every beam, leg, cam, and caster in the system, sold individually. Fix anything, extend anything, or build something nobody's thought of yet. Custom length I-beams and any leg height on request.",
    title: 'Benchwork Parts: I-Beams, Legs, Cams | Mianne Benchwork',
    description:
      'Every part in the Mianne system sold individually, with prices. Custom lengths and heights on request.',
    hero: 'hero-parts',
    heroAlt: 'Mianne I-beams, legs, and cam fasteners laid out on a workbench',
    tile: 'PARTS & ACCESSORIES',
    tileSub: 'Beams, legs, cams, casters',
    widthFilter: false,
  },
  accessories: {
    h1: 'Lift-Gates, Multi-Deck & More',
    intro:
      'The catalog goes further than the kits. A motorized Lift-Gate that raises a section of benchwork out of your path. A cantilevered second deck that adds up to 75 percent more layout over the same floor. Transformer shelves and rollaway carts to keep the power where your hand expects it.',
    title: 'Lift-Gates, Multi-Deck & Accessories | Mianne Benchwork',
    description:
      'Motorized Lift-Gates, cantilevered second decks, transformer shelves and rollaway carts for Mianne layouts.',
    hero: 'hero-accessories',
    heroAlt: 'Two-level Mianne benchwork with a cantilevered upper deck over a sceniced main level',
    tile: 'LIFT-GATES & MULTI-DECK',
    tileSub: 'Lift-Gates, second decks, shelves, carts',
    widthFilter: false,
  },
};
