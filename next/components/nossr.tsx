import { FC, Fragment } from "react"
import dynamic from 'next/dynamic'

export const NoSsr: FC = ({ children }) => {
  const Frag = () =>
    <Fragment>{children}</Fragment>
  return (
    <>{dynamic(() => Promise.resolve(Frag), {
      ssr: false
    })}</>
  )
}
