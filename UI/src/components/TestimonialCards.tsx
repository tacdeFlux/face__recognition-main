"use client";
import { InfiniteMovingCards } from "./ui/infinite-moving-cards";

const musicTestimonialCard = [
  {
    quote:
      "My focus was on designing responsive layouts and user-friendly features, connecting the interface with Python to enable real-time attendance updates efficiently",
    name: "Tanya Modi",
    title: "Software engineer",
  },
  {
    quote:
      "I created an intuitive user interface that enhances user experience and simplifies attendance management, ensuring seamless interaction with the backend system.",
    name: "Ankit Kumar",
    title: "Software engineer",
  },
  {
    quote:
      "I developed a robust face recognition model using Python, implementing advanced algorithms to achieve high accuracy and reliability in attendance tracking.",
    name: "Sumit Shukla",
    title: "Software engineer",
  },
  {
    quote:
      "My role involved optimizing the model's performance, fine-tuning parameters to ensure it accurately identifies faces and minimizes false positives during attendance recording.",
    name: "Nishu",
    title: "Software engineer",
  },
];

const TestimonialCards = () => {
  return (
    <div className="h-[40rem] w-full dark:bg-black dark:bg-grid-white/[0.2] relative flex flex-col items-center justify-center overflow-hidden">
      <h2 className="text-3xl font-bold text-center mb-8 z-10">
        "Software Engineer: The Future of Attendance Management"
      </h2>
      <div className="flex justify-center w-full overflow-hidden px-4 sm:px-6 lg:px-8">
        <div className="w-full max-w-6xl">
          <InfiniteMovingCards
            items={musicTestimonialCard}
            direction="right"
            speed="slow"
          />
        </div>
      </div>
    </div>
  );
};

export default TestimonialCards;
