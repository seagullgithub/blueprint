import React from 'react';
import { useRef, useEffect } from 'react';

export default function Sketch(){

  const refCanvas = useRef(null);
  let ctx;

  useEffect(() => {
     ctx = refCanvas.current.getContext("2d");
  });

  return( <>
    <canvas
      ref={refCanvas}
    ></canvas>
  </>)
}
