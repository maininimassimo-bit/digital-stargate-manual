import { readFile, writeFile } from 'node:fs/promises';
import process from 'node:process';

const SESSIONS_PATH = 'data/analytics/history/sessions.csv';
const TARGETS_PATH = 'data/analytics/history/targets.csv';
const METADATA_PATH = 'data/analytics/metadata/session-scientific-metadata.csv';
const OUTPUT_PATH = 'docs/data/sc