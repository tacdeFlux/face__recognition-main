"use client";
import React from "react";
import { StickyScroll } from "./ui/sticky-scroll-reveal";

const musicSchoolContent = [
  {
    title: "Real-Time Attendance",
    description:
      "The Real-Time Attendance feature captures and records attendance instantly as individuals arrive, enabling immediate updates to attendance records, enhancing accuracy, and streamlining administrative processes.",
  },
  {
    title: "Offline Image Storage and Backup",
    description:
      "The Offline Image Storage and Backup feature securely saves face images locally, ensuring data privacy and accessibility, while providing reliable backups without needing an internet connection.",
  },
  {
    title: "Spreadsheet Attendance Analytics",
    description:
      "The Spreadsheet Attendance Analytics feature processes attendance data, generating insightful reports and visualizations to help identify trends, improve attendance management, and enhance decision-making.",
  },
  {
    title: "High Accuracy",
    description:
      "The High Accuracy feature utilizes advanced algorithms and models to ensure precise facial recognition, significantly reducing false positives and enhancing the reliability of attendance records.",
  },
];
const ChooseUs = () => {
  return (
    <div className="">
      <StickyScroll content={musicSchoolContent} />
    </div>
  );
};

export default ChooseUs;
