import { useEffect, type RefObject } from "react";

export default function useOutsideAlerter(ref: RefObject<HTMLElement | null>, callBackFunction: Function) {
  useEffect(() => {

    console.log(ref);

    function handleClickOutside(event: MouseEvent) {
      if (ref.current && !ref.current.contains(event.target as Node)) {
        callBackFunction();
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [ref, callBackFunction]);
}