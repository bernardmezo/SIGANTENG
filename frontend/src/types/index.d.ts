export {};

declare global {
  interface CustomJwtSession {
    accessToken?: string;
    refreshToken?: string;
    error?: string;
  }
}
