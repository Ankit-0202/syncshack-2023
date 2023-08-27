# Slidey

A Chrome extension for presentations made using Google Slides that leverages the capabilities of AI.

## Table of Contents

- [Problem Statement](#problem-statement)
- [Introducing Slidey: Simplifying Presentation Production](#introducing-slidey-simplifying-presentation-production)
- [How does Slidey work?](#how-does-slidey-work)
- [Who Can Use Slidey?](#who-can-use-slidey)
- [Prototype Overview](#prototype-overview)
- [How Slidey Operates](#how-slidey-operates)
- [Experience Slidey For Yourself!](#experience-slidey-for-yourself)
    - [Installation Guide](#installation-guide)

## Problem Statement

In an era marked by the constant emergence of new ideas and concepts, effective presentation of knowledge holds paramount importance. However, the process of creating engaging presentations remains a daunting and time-intensive task, diverting valuable efforts and resources away from other productive endeavours.

## Introducing Slidey: Simplifying Presentation Production

**Slidey** addresses the challenge of presentation creation head-on. By harnessing the capabilities of Language Models (LLMs), quantum bits and text-to-image generation, Slidey revolutionises the way presentations are crafted. Gone are the days of intricate and laborious slide design processes. With Slidey, producing captivating slides for demonstrations and research becomes effortlessly efficient.

## How does Slidey work?

Slidey offers a user-friendly Chrome extension that streamlines the presentation preparation process. Here's how it works:

1. **Prompt and Mood:** Start by providing a prompt and specifying the desired mood or tone of your presentation.

2. **Google Account Integration:** Log in to your Google account and open a presentation where you intend to incorporate the slides.

3. **Automated Content Generation:** Slidey takes it from there, generating content, speaker notes, and complementary images tailored to enhance your presentation's impact.

## Who Can Use Slidey?

Slidey is designed to cater to a wide spectrum of users eager to share information effectively. Its intuitive interface makes it accessible to users of all demographics, from young presenters just starting out to full-blown professionals. Specifically, Slidey caters to:

- Individuals looking to create quick and engaging presentations for informal occasions.
- Those seeking a template to build comprehensive and visually appealing slideshows for more complex presentations.

## Prototype Overview

Our prototype is a Chrome extension that taps into Google's API to craft dynamic and compelling slideshows. With just a concept and a desired tone, Slidey generates a cohesive set of assets, including images, speaker notes, and concise text for each slide.

## How Slidey Operates

Slidey operates through an amalgamation of AI technologies:

1. **Prompts and AI Tools:** The extension utilizes a series of prompts that synergize outputs from diverse AI tools, including the prowess of OpenAI and Stable Diffusion.

2. **Langchain Model:** The generated content undergoes refinement through a langchain model, ensuring coherence and relevance.

3. **Seamless Integration:** Finally, the refined content seamlessly integrates with a Google Slides presentation, ready to captivate and inform your audience.

## Experience Slidey For Yourself!

Ready to transform your presentation creation process? Clone our Git repository and access Slidey today:

[Slidey Repository](https://github.com/Ankit-0202/syncshack-2023.git)

### Installation Guide

Once you've pulled the repository, follow these steps to use Slidey:

### Installation Guide

Once you've pulled the repository, follow these steps to use Slidey:

1. Enter the directory and install all of the necessary dependencies.

    ```bash
    # Change directory and install dependencies using pip3 and npm
    cd syncshack-2023
    make install      # command installs all dependencies for you
    ```

2. Build the backend and frontend in separate terminals.

    In one directory:

    ```bash
    cd syncshack-2023
    make backend
    ```

    and in another:

    ```bash
    cd syncshack-2023
    make frontend
    ```

    You will need to have both terminals running in order to use Slidey.

3. Load the extension into Chrome.

    3.1. Open Google Chrome and go to [chrome://extensions/](chrome://extensions/).
    ![Extensions page on Google Chrome](https://github.com/Ankit-0202/syncshack-2023/blob/main/resources/extensions_page.png)

    3.2. Enable "Developer mode" at the top right corner.
    ![Developer tools on the extensions page for Chrome](https://github.com/Ankit-0202/syncshack-2023/blob/main/resources/dev_tools.png)

    3.3. Click the "Load unpacked" button.

    3.4. Select the `dist` directory in the `syncshack-2023` repository.

4. Open Slidey.

    You should now see your extension icon in the Chrome extension toolbar.
    ![Open Slidey!] (https://github.com/Ankit-0202/syncshack-2023/blob/main/resources/choose_slidey.png)

    Make sure that when you run Slidey you are on a Google Slide presentation!

We hope you enjoy using Slidey!