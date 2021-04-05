import React, { FC, Fragment } from "react"

import "@google/model-viewer/dist/model-viewer";
import dynamic from "next/dynamic";

declare global {
  namespace JSX {
    interface IntrinsicElements {
      'model-viewer': ModelViewerJSX & React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement>, HTMLElement>;
    }
  }
}

interface ModelViewerJSX {
  src: string
  poster?: string
  'auto-rotate'?: boolean
  'autoplay'?: boolean
  'camera-controls'?: boolean
  // ... others
}

export const Model: FC<{ fileName: string, props: React.HTMLAttributes<HTMLElement> }> = ({ fileName, props }) => (
  <model-viewer {...props} src={fileName} camera-controls autoplay />
)

export default Model
