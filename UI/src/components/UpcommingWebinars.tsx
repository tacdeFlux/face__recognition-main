"use client";
import Link from "next/link";
import { HoverEffect } from "./ui/card-hover-effect";

const UpcommingWebinars = () => {
  const featuredWebinar = [
    {
      title: "Understanding the concept of ReactJS",
      description:
        "React.js is a JavaScript library for building user interfaces, known for its component-based architecture and virtual DOM.",
      slug: "Understanding-the-programming",
      isFeatured: true,
    },
    {
      title: "Understanding the concept of TailwindCSS",
      description:
        "Tailwind CSS streamlines web development with utility-first classes for rapid and customizable styling.",
      slug: "Understanding-the-programming",
      isFeatured: true,
    },

    {
      title: "Understanding the concept of Typescript",
      description:
        "TypeScript is a superset of JavaScript that adds static typing for improved code quality and maintainability.",
      slug: "Understanding-the-programming",
      isFeatured: true,
    },
  ];
  return (
    <div className="p-12 bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="text-center">
          <h2 className="text-base text-teal-600 font-semibold tracking-wide uppercase">
            Learning
          </h2>
          <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-white sm:text-4xl">
            Enhance Our Project Journey
          </p>
        </div>

        <div className="mt-10">
          <HoverEffect
            items={featuredWebinar.map((webinar) => ({
              title: webinar.title,
              description: webinar.description,
              link: "/",
            }))}
          />
        </div>
      </div>
    </div>
  );
};

export default UpcommingWebinars;
