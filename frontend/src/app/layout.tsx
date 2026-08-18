import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL("https://vitaliipavlii.com"),
  title: {
    default: "Vitalii Pavlii — Senior Full-Stack Software Engineer",
    template: "%s | Vitalii Pavlii",
  },
  description:
    "Senior full-stack software engineer with 10+ years of experience building reliable products, distributed systems, and delivery processes.",
  authors: [{ name: "Vitalii Pavlii", url: "https://vitaliipavlii.com" }],
  creator: "Vitalii Pavlii",
  alternates: {
    canonical: "/",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
    },
  },
  openGraph: {
    type: "website",
    url: "/",
    siteName: "Vitalii Pavlii — Portfolio",
    title: "Vitalii Pavlii — Senior Full-Stack Software Engineer",
    description:
      "Senior full-stack software engineer building reliable products, distributed systems, and delivery processes.",
  },
  twitter: {
    card: "summary_large_image",
    title: "Vitalii Pavlii — Senior Full-Stack Software Engineer",
    description:
      "Senior full-stack software engineer building reliable products, distributed systems, and delivery processes.",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
