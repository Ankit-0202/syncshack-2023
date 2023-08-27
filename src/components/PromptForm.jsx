import { useState } from 'react';
import { Box, Button, CircularProgress, Grid, TextField } from '@mui/material';
// import { io } from 'socket.io-client';

// const URL = process.env.NODE_ENV === 'production' ? undefined : 'http://localhost:4000';

const GOOGLE_SLIDES_URL_REGEX =
    /https:\/\/docs\.google\.com\/presentation\/d\/([a-zA-Z0-9_-]+)\/edit#slide=id.([a-zA-Z0-9_-]+)/;

// export const socketio = io(URL);

export default function PromptForm() {
  const [generating, setGenerating] = useState(false);
  const [generateSuccessful, setGenerateSuccessful] = useState(false);
  const [prompt, setPrompt] = useState("");
  const [mood, setMood] = useState("");

  function clearForm() {
    setPrompt("");
    setMood("");
  }

  function submitPrompt(event) {
    event.preventDefault();

    if (!generating) {
      setGenerateSuccessful(false);
      setGenerating(true);
    }

    chrome.tabs.query({active: true, currentWindow: true})
        .then(([tab]) => {
          // const [, presentationID, slidePageID] = GOOGLE_SLIDES_URL_REGEX.exec(tab.url);
          const regexMatch = GOOGLE_SLIDES_URL_REGEX.exec(tab.url);
          if (regexMatch) {
            const presentationID = regexMatch[1];
            const slidePageID = regexMatch[2];
            console.log("matched");
            return chrome.scripting.executeScript({
              target: {tabId: tab.id},
              func: (paramPresentationID, paramSlidePageID) => {
                const SELECTED_ELEMENT_COLOUR = "#8ab4f8";
                const selectedElementDOMElement =
                    document.querySelector(`path[stroke="${SELECTED_ELEMENT_COLOUR}"]`);

                // If no element is selected, return null
                if (selectedElementDOMElement === null) {
                  return {
                    presentationID: paramPresentationID,
                    pageID: paramSlidePageID,
                    paramSlidePageIDobjectID: null,
                  };
                }

                // Parent is 3 nodes above
                let targetElement = selectedElementDOMElement;
                while (!targetElement.hasAttribute("id")) {
                  targetElement = targetElement.parentElement;
                }

                // Now, get the object ID from the `id` attribute
                const objectID = targetElement.id;
                return {
                  presentationID: paramPresentationID,
                  pageID: paramSlidePageID,
                  objectID,
                };
              },
              args: [presentationID, slidePageID],
            });
          } else {
            return null;
          }
        }).then((results) => {
          const selectedObjectID = results !== null ? results[0].result : null;
          const jsonData = {
            prompt,
            mood,
          };

          if (selectedObjectID) {
            const {presentationID, pageID, objectID} = selectedObjectID;
            jsonData.presentationID = presentationID;
            jsonData.pageID = pageID;
            jsonData.objectID = objectID;
          } else {
            jsonData.presentationID = null;
            jsonData.pageID = null;
            jsonData.objectID = null;
          }
          
          return jsonData;
        }).then((jsonData) => {
          return fetch("http://localhost:5000/prompt-processing", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(jsonData),
          });
        }).then((data) => {
          return data.json();
        }).then((jsonResponseData) => {
          if (jsonResponseData.status != "OK") {
            throw new Error("bad status");
          }
        }).then(() => {
          setGenerateSuccessful(true);
          setGenerating(false);
          clearForm();
        }).catch((error) => {
          console.error(error);
        });
  }

  return (
    <Grid
      component="form"
      container
      spacing={2}
      onSubmit={submitPrompt}
    >
      <Grid item xs={12}>
        <TextField
          id="prompt-input"
          label="Prompt input"
          multiline
          fullWidth
          size="small"
          value={prompt}
          disabled={generating}
          onChange={(e) => setPrompt(e.target.value)}
        />
      </Grid>

      <Grid item xs={12}>
        <TextField
          id="mood-input"
          label="Mood"
          helperText="Enter a mood to jazz up your presentation!"
          fullWidth
          size="small"
          value={mood}
          disabled={generating}
          onChange={(e) => setMood(e.target.value)}
        />
      </Grid>

      <Grid item xs={12}>
        <Box sx={{m: 1, position: "relative"}}>
          <Button
            type="submit"
            variant="contained"
            disabled={generating}
          >
            Send Prompt
          </Button>
          {generating && (
            <CircularProgress
              size={24}
              sx={{
                position: "absolute",
                top: "50%",
                left: "50%",
                marginTop: "-12px",
                marginLeft: "-12px",
              }}
            />
          )}
        </Box>
      </Grid>
    </Grid>
  );
}
