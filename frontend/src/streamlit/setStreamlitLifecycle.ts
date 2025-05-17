import { onMount, afterUpdate } from "svelte";
import { Streamlit } from "./streamlit";

export const setStreamlitLifecycle = (): void => {
  onMount((): void => {
    Streamlit.setFrameHeight();
  });

  afterUpdate((): void => {
    // In here I tell Streamlit to update my frameHeight after each update, in
    // case it has changed. (This isn't strictly necessary for the example
    // because our height stays fixed, but this is a low-cost function, so
    // there's no harm in doing it redundantly.)
    Streamlit.setFrameHeight();
  });
};
