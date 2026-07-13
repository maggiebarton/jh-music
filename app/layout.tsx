import type { Metadata } from "next";
import type { ReactNode } from "react";
import "./globals.css";

export const metadata: Metadata = {
  title: "Joshua T. Hester | Americana & Folk Singer-Songwriter",
  description:
    "The official website of Wisconsin Americana and folk singer-songwriter Joshua T. Hester.",
};

export default function RootLayout({ children }: Readonly<{ children: ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
