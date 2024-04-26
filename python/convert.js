import { writeFileSync } from 'fs';
import sortedPoems from '../public/Poems_sorted.js';

writeFileSync('poems_sorted.json', JSON.stringify(sortedPoems));