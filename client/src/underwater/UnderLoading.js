import React from "react";
import { GiSandsOfTime } from "react-icons/gi";
import "./css/style.css";
import { motion } from "framer-motion";

export default function UnderLoading() {
  return (
    <div className="u-container">
      <div className="u-titlecenter">
        <motion.div
          animate={{
            opacity: [1, 0.8, 0.6, 0.4, 0.2, 0.1, 0.2, 0.4, 0.6, 0.8, 1],
          }}
          transition={{ repeat: Infinity, repeatDelay: 3, duration: 1 }}
        >
          Waiting for players...
        </motion.div>
      </div>
      <div className="u-motion-container">
        <motion.div
          animate={{ rotate: [0, 180, 180, 0] }}
          transition={{ repeat: Infinity, repeatDelay: 1.5, duration: 1.5 }}
        >
          <GiSandsOfTime size="50px" />
        </motion.div>
      </div>
    </div>
  );
}
