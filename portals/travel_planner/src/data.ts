import europe from './components/assets/europe.jpg';
import asia from './components/assets/asia.jpg';
import africa from './components/assets/africa.jpg';
import southAmerica from './components/assets/south-america.jpg';
import centralAmerica from './components/assets/central-america.jpg';
import northAmerica from './components/assets/north-america.jpg';
import middleEast from './components/assets/middle-east.jpg';
import oceania from './components/assets/oceania.jpg';
import albania from './components/assets/albania.jpg'
import armenia from './components/assets/armenia.jpg'
import austria from './components/assets/austria.jpg'


interface Region {
  regionName: string;
  regionSummary: string;
  regionImage: string;
}

interface Country {
  countryName: string;
  countryImage: string;
}

interface RegionDetails {
  regionName: string;
  regionDescription: string;
  regionImage: string;
  regionCountries: Country[]
}

export const regions: Region[] = [
  {
    regionName: "Europe",
    regionImage: europe,
    regionSummary: "Explore the diverse cultures, rich history, and stunning landscapes of Europe.",
  },
  {
    regionName: "Asia",
    regionImage: asia,
    regionSummary: "Discover the ancient traditions, bustling cities, and breathtaking landscapes of Asia.",
  },
  {
    regionName: "Africa",
    regionImage: africa,
    regionSummary: "Experience the vibrant cultures, diverse wildlife, and stunning landscapes of Africa.",
  },
  {
    regionName: "Middle East",
    regionImage: middleEast,
    regionSummary: "Explore the historical sites, cultural diversity, and natural beauty of the Middle East.",
  },
  {
    regionName: "North America",
    regionImage: northAmerica,
    regionSummary: "Discover the natural wonders, diverse cultures, and bustling cities of North America.",
  },
  {
    regionName: "Central America",
    regionImage: centralAmerica,
    regionSummary: "Experience the rich history, vibrant cultures, and stunning landscapes of Central America.",
  },
  {
    regionName: "South America",
    regionImage: southAmerica,
    regionSummary: "Explore the diverse landscapes, rich history, and vibrant cultures of South America.",
  },
  {
    regionName: "Oceania",
    regionImage: oceania,
    regionSummary: "Discover the stunning islands, unique wildlife, and diverse cultures of Oceania.",
  },

];

export const regionsData: RegionDetails[] = [
  {
      regionName: "Europe",
      regionImage: europe,
      regionDescription: "Europe has some of the best destinations in the world. Ranging from cities with rich history, beautiful beach destinations, areas with breathtaking landscapes, incredible ski resorts and so much more.<br> Through this section of the website you’ll be able to find posts on European destinations. Some of these posts are detailed city break guides, which help you plan a trip to a city, and provide ideas on things to see and do, suggestions on places to eat, where to stay, photography tips and more.<br> You’ll also find some posts with ideas, such as cities that are extremely photogenic, and destinations that are very romantic. For some destinations, we have picture-based posts, which show you photographs to give you an idea of what to expect, as well as a little bit of information on the destination.<br> Finally towards the end you’ll find links to posts that provide travel tips. Such as for your first time travelling in Europe, how to plan a multi-destination trip and how to save money whilst travelling.",
      regionCountries: [
        {countryName: "Albania", countryImage: albania},
        {countryName:"Armenia", countryImage: armenia},
        {countryName:"Austria", countryImage: austria},
      ],
  },
  {
      regionName: "Asia",
      regionImage: europe,
      regionDescription: "dadada",
      regionCountries: [
        {countryName:"1222", countryImage: albania},
        {countryName:"2333", countryImage: albania}
      ]
  }
];