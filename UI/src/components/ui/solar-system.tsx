"use client";
import React, { useState, useEffect, useRef } from "react";
import { motion } from "framer-motion";

interface Star {
  id: number;
  initialX: number;
  initialY: number;
  x: number;
  y: number;
  size: number;
  opacity: number;
}

interface ShootingStar {
  id: number;
  startX: number;
  startY: number;
  endX: number;
  endY: number;
  duration: number;
  delay: number;
}

export const SolarSystem = () => {
  const [stars, setStars] = useState<Star[]>([]);
  const [shootingStars, setShootingStars] = useState<ShootingStar[]>([]);
  const containerRef = useRef<HTMLDivElement>(null);

  // Initialize stars
  useEffect(() => {
    const initialStars = [...Array(700)].map((_, i) => ({
      id: i,
      initialX: Math.random() * window.innerWidth,
      initialY: Math.random() * window.innerHeight,
      x: Math.random() * window.innerWidth,
      y: Math.random() * window.innerHeight,
      size: Math.random() * 3.5 + 1,
      opacity: Math.random() * 0.7 + 0.3,
    }));
    setStars(initialStars);
  }, []);

  return (
    <div
      ref={containerRef}
      className="fixed inset-0 w-full h-full overflow-hidden pointer-events-none"
    >
      {/* Interactive stars */}
      {stars.map((star) => (
        <motion.div
          key={star.id}
          className="absolute bg-white rounded-full shadow-lg"
          style={{
            width: `${star.size}px`,
            height: `${star.size}px`,
            left: `${star.initialX}px`,
            top: `${star.initialY}px`,
            boxShadow: `0 0 ${star.size * 3}px rgba(255, 255, 255, ${star.opacity}), 0 0 ${star.size * 6}px rgba(100, 200, 255, ${star.opacity * 0.6})`,
          }}
          animate={{
            opacity: [star.opacity * 0.4, star.opacity, star.opacity * 0.4],
            scale: [0.8, 1.2, 0.8],
          }}
          transition={{
            duration: Math.random() * 4 + 2.5,
            repeat: Infinity,
            delay: Math.random() * 2,
            ease: "easeInOut",
          }}
        />
      ))}
    </div>
  );
};
