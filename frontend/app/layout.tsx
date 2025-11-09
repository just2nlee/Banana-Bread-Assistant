import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Banana Bread Assistant - Know When Your Banana is Bake-Ready',
  description: 'Upload a banana photo to predict when it will be perfect for baking banana bread!',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

