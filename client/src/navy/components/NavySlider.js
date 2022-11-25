import React, { useState } from "react";
import NavySlide1 from "./NavySlide1";
import NavySlide2 from "./NavySlide2";
import "./NavySlider.css";
import "./../index.css";

const NavySlider = () => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const slides = [<NavySlide1 />, <NavySlide2 />];

  const goToPrevious = () => {
    const isFirst = currentIndex === 0;
    const newIndex = isFirst ? slides.length - 1 : currentIndex - 1;
    setCurrentIndex(newIndex);
  };

  const goToNext = () => {
    const isFirst = currentIndex === slides.length - 1;
    const newIndex = isFirst ? 0 : currentIndex + 1;
    setCurrentIndex(newIndex);
  };

  const goToSlide = (slideIndex) => {
    setCurrentIndex(slideIndex);
  };

  return (
    <div>
      <div className="row align-items-center navy-slider-container navy-text">
        <div className="col-1 arrow-slide left-arrow-slide" onClick={goToPrevious}>
          ❰
        </div>
        <div className="col">{slides[currentIndex]}</div>
        <div className="col-1 arrow-slide right-arrow-slide" onClick={goToNext}>
          ❱
        </div>
      </div>
      <div className="dots-container">
        {slides.map((slide, slideIndex) => (
          <div
            key={slideIndex}
            className="dots"
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
