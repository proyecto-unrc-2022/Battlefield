import React, { useState } from "react";
import "./../../index.css";
import "./NavySlider.css";
import NavySlide1 from "./NavySlide1";
import NavySlide2 from "./NavySlide2";
import NavySlide3 from "./NavySlide3";
import NavySlide4 from "./NavySlide4";
import NavySlide5 from "./NavySlide5";
import NavySlide6 from "./NavySlide6";

const NavySlider = () => {
  const slides = [
    <NavySlide1 />,
    <NavySlide2 />,
    <NavySlide3 />,
    <NavySlide4 />,
    <NavySlide5 />,
    <NavySlide6 />,
  ];
  const [currentIndex, setCurrentIndex] = useState(0);
  const [currentSlide, setCurrentSlide] = useState(slides[currentIndex]);

  const goToPrevious = () => {
    const isFirst = currentIndex === 0;
    const newIndex = isFirst ? slides.length - 1 : currentIndex - 1;
    setCurrentSlide(slides[newIndex]);
    setCurrentIndex(newIndex);
  };

  const goToNext = () => {
    const isFirst = currentIndex === slides.length - 1;
    const newIndex = isFirst ? 0 : currentIndex + 1;
    setCurrentSlide(slides[newIndex]);
    setCurrentIndex(newIndex);
  };

  const goToSlide = (slideIndex) => {
    setCurrentSlide(slides[slideIndex]);
    setCurrentIndex(slideIndex);
  };

  return (
    <div>
      <div className="row align-items-center navy-slider-container navy-text">
        <div
          className="col-1 arrow-slide left-arrow-slide"
          onClick={goToPrevious}
        >
          ❰
        </div>
        <div className="col">{currentSlide}</div>
        <div className="col-1 arrow-slide right-arrow-slide" onClick={goToNext}>
          ❱
        </div>
      </div>
      <div className="dots-container">
        {slides.map((slide, slideIndex) => (
          <div
            key={slideIndex}
            className={"dots " + (currentIndex === slideIndex ? "hover-dot" : "")}
            onClick={() => goToSlide(slideIndex)}
          >
            ●
          </div>
        ))}
      </div>
    </div>
  );
};

export default NavySlider;
