/*
 *
 * This file holds constants for field positions for alert data.
 *
 * */

const ID = 0;
const DATE = 1;
const ZIP = 2;
const CITY = 3;
const STATE = 4;
const COUNTRY = 5;
const TYPE = 6;
const DESC = 7;
const SEVERITY = 8;
const AUTHOR = 9;
const ACTIVE = 10;
const BLACK = "#000000";
const YELLOW = "#FFCC00";
const RED =  "#CC0000";
const WHITE = "FFFFFF"
const DEFAULT_WIDTH = 450
const HEADER_WIDTH = 5;
const PADDING = "2%";
const flds = { DATE, ID, ZIP, CITY, STATE, COUNTRY, TYPE, DESC, SEVERITY,
              AUTHOR, ACTIVE };

const colors = { BLACK, YELLOW, RED, WHITE };

const sizes = { DEFAULT_WIDTH, HEADER_WIDTH, PADDING };

export { flds as default, colors, sizes };
