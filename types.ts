

export type FilmData = Film[]

export interface Film {
  filmName: string,
  href: string,
  screens: Screening
}

export interface Screening {
  day0?: Screen[]
}

export interface Screen {
  screenType: string,
  screenFeatures: ScreenFeatures[],
  showTimes: Showtime[],
}

export enum ScreenFeatures{
  RECLINERS = "AMC Signature Recliners",
  A_LIST_EXCLUSION = "Excluded from A-List",
  MOVIE_SELECTION = "Choose from Our Available Movie Selection",
  RESERVED_SEATING = "Reserved Seating",
  CLOSED_CAPTION =  "Closed Caption",
  AUDIO_DESCRIBED = "Audio Description"

}

export interface Showtime {
  time: string,
  href: string
}