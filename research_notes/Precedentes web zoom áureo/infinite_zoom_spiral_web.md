# Precedents: infinite-zoom and golden-spiral / golden-rectangle scroll navigation on the web

Research date: 2026-10-06. Method note: the network proxy blocked direct fetches of codepen.io, awwwards.com, fastcompany.com, commarts.com, narrowdesign.com, zoomquilt.org, loadmo.re and geogebra.org. Only the GitHub Gist (gist.github.com) was fetched and read directly ("VERIFIED"). Everything else comes from search-engine result snippets ("SNIPPET", which means the claim was attributed to the cited page by the search engine but I did not read the page myself). Treat SNIPPET items as likely but unconfirmed.

## Q1. Which infinite-zoom web projects exist, and how do they work (scroll-driven or autoplay, looping)?

### Takeaway
Infinite-zoom art on the web is an established genre. It began with Zoomquilt (Nikolaus Baumgarten and collaborators, mid-2000s) and continued with Zoomquilt 2 (2007) and Arkadia (2015). Since 2022 it has become a mass trend through AI outpainting tools. All of these are image-content loops: the zoom is continuous, the last image contains the first, and the frame does not rotate. None of them uses golden-rectangle geometry.

### Cited Findings
- Zoomquilt (zoomquilt.org) is a collaborative infinitely zooming image. Its credits name Nikolaus Baumgarten as the organiser. SNIPPET — [Zoomquilt](https://zoomquilt.org/); [Cogimator listing](https://cogimator.net/en/sites/zzz-zoomquilt-org/)
- Zoomquilt works like a stack of cards, each with a hole in it, where "the last card is also the one before the first". This is what makes it loop seamlessly. Each artwork contains a smaller version of the next scene. SNIPPET — [Unity gist by steve-salmond describing the Zoom Quilt technique](https://gist.github.com/steve-salmond/5952537); [Curiouxify explainer](https://curiouxify.com/zoomquilt-explained/)
- The zoom runs on its own and never stops. There is no loading page and no button. The search snippet says nothing about user controls. Other sources say the user can speed it up or reverse it with the mouse wheel or arrow keys, but I could not verify that. SNIPPET — [Curiouxify](https://curiouxify.com/zoomquilt-explained/); [Plymouth "Tide Talk"](https://wrasse.plymouth.ac.uk/ac-news/zoomquilt-org-a-deep-dive-into-infinite-zoom-art-1764803136)
- Zoomquilt 2 was released in 2007 at zzz.zoomquilt2.com. Arkadia (zzz.arkadia.xyz) was made in 2015 by Baumgarten with painter Sophia Schomberg. SNIPPET — [Zoomquilt 2](https://zzz.zoomquilt2.com/); [Arkadia](https://zzz.arkadia.xyz/); [Transylvania Univ. "Loop" exhibition bio](https://morlan.transy.edu/loop2021/nikolaus-baumgarten/)
- Zoomquilt has also shipped as a Mac App Store app. SNIPPET — [App Store](https://apps.apple.com/us/app/zoomquilt/id6454792945?mt=12)
- A 2013 Hacker News thread on Zoomquilt shows it was already well known in tech circles. SNIPPET — [HN item 6542450](https://news.ycombinator.com/item?id=6542450)
- AI infinite zoom (from about 2022 onward): the AUTOMATIC1111 "infinite-zoom" extension and similar tools shrink the image into the centre and outpaint the border, step after step, to make zoom videos. Apps such as Videoleap sell this for social-media video. These are autoplay videos and are not scroll-navigated sites. SNIPPET — [v8hid/infinite-zoom-automatic1111-webui](https://github.com/v8hid/infinite-zoom-automatic1111-webui); [PhilSad SD outpainting video](https://github.com/PhilSad/stable-diffusion-infinite-outpainting-video); [Videoleap Infinite Zoom](https://www.videoleapapp.com/tools/infinite-zoom-ai); [revid.ai "infinite zoom loop / Droste effect" generator](https://www.revid.ai/make/ai-infinite-zoom-loop-droste-effect)
- Droste-effect tools and short videos are common: an "Infinite Zoom UI Animation (Droste Effect)" YouTube Short and a free Droste maker. The Droste-effect explainer notes that Escher's *Print Gallery* bends the recursion into a logarithmic spiral. SNIPPET — [YouTube Short](https://www.youtube.com/shorts/1kH2IPKA58o); [zlabz Droste maker](https://zlabz.io/en/droste)
- Looping fractal-zoom videos (2014) and a real-life "infinite fractal zoom" camera shot (PetaPixel, May 2023) exist. SNIPPET — [The Alpha Blenders](https://thealphablenders.com/2014/11/looping-fractal-zooms/); [PetaPixel](https://petapixel.com/2023/05/17/this-real-life-infinite-fractal-zoom-shot-looks-like-cgi-but-its-real/)

### Inferences
- "Endless looping zoom" by itself is not new. It has been a known web art form for about 20 years and a social-video cliché since 2022. Anything new in the concept has to come from the golden-rectangle geometry, the rotation, and the use of the zoom as studio-portfolio navigation.
- Zoomquilt's "last card is the one before the first" technique is exactly the looping mechanism the concept needs. The golden rectangle gives this self-similarity geometrically, so no painted transitions are required.

### Gaps
- I could not open zoomquilt.org to verify the exact original launch year (often cited as 2004) or the scroll and keyboard controls.
- I did not find documented Instagram/Reels trend data with dates, beyond the AI tool pages.

## Q2. Are there websites or portfolios (Awwwards/FWA/CSSDA) whose scroll navigation follows a golden spiral or zooms into golden-rectangle squares?

### Takeaway
Yes, and it is very close to the concept. Nick Jones's portfolio at **narrowdesign.com** (Narrow Design, North Carolina, 2017) uses scroll to zoom from one golden-rectangle square to the next with a 90° rotation per step. It was Awwwards Site of the Day on 30 May 2017, was covered by Fast Company in 2017, and went viral on Twitter. I found no other award-site examples of golden-spiral navigation.

### Cited Findings
- Jones's own words, as quoted by Fast Company: "The golden spiral is a familiar visual form to both designers and nondesigners alike, and I always thought it'd be a great way to do a layout… by zooming from one square to the next and rotating 90 degrees, I could build an infinitely deep interface." SNIPPET — [Fast Company, "7 Design Portfolios That Double As Awesome UIs" (2017)](https://www.fastcompany.com/90125529/7-design-portfolios-that-double-as-awesome-uis)
- On the live site, the page "literally rotates to the left" as you scroll. Tiles form a spiral that you descend and ascend by scrolling, zooming in and out along the golden/Fibonacci spiral. The site went viral on Twitter and had more than 100,000 visitors in its launch week. Some people got vertigo from it, so Jones added a more "accessible" (non-spiral) version. He built it in plain HTML/CSS/JS with no WebGL or React. SNIPPET — [Fast Company](https://www.fastcompany.com/90125529/7-design-portfolios-that-double-as-awesome-uis); [Communication Arts Webpick "Nick Jones"](https://www.commarts.com/webpicks/nick-jones)
- Awwwards: "Nick Jones Design and Code" was Site of the Day on 30 May 2017 with a score of 7.64. It is described as a "single page website [with] a spiraling and zooming canvas of content". Awwwards tags include "Golden Spiral" and "Golden Ratio Grid Navigation". There is a second entry, "Nick Jones / Design + Code". SNIPPET — [Awwwards SOTD](https://www.awwwards.com/sites/nick-jones-design-and-code); [Awwwards second entry](https://www.awwwards.com/sites/nick-jones-design-code)
- Other coverage: Dribbble shot "Nick Jones — Design and Code" (no. 3498350, about mid-2017), One Page Love, a Webflow forum thread "Impressive website by Nick Jones", Kevin Bizien's blog, and loadmo.re. SNIPPET — [Dribbble](https://dribbble.com/shots/3498350-Nick-Jones-Design-and-Code); [One Page Love](https://onepagelove.com/nick-jones); [Webflow forum](https://discourse.webflow.com/t/impressive-website-by-nick-jones/42904); [kevinbizien.com](https://kevinbizien.com/en/sharing/narrowdesign-dot-com); [loadmo.re](https://loadmo.re/posts/narrow-design)
- Other Awwwards zoom-scroll entries exist, but they are generic zoom transitions, not golden geometry. One example is "Scroll navigation zoom in effect – Ocus" (tags: scrolling, fullscreen, infinite scroll). SNIPPET — [Awwwards inspiration: Ocus](https://www.awwwards.com/inspiration/scroll-navigation-zoom-in-effect-ocus)

### Inferences
- narrowdesign.com is the direct precedent. It uses the same core geometric move as the concept (scale by φ, rotate 90°, enter the next square, driven by scroll), and it is a designer's portfolio. It was highly visible in the industry: Awwwards SOTD, Fast Company, CommArts, and over 100k visitors. Any informed design-press or Awwwards jury will likely recognise the reference.
- The vertigo and accessibility backlash is a documented lesson for the new concept. Plan a reduced-motion path (prefers-reduced-motion) from the start.

### Gaps
- I could not load narrowdesign.com to confirm whether the spiral version is still live in 2026, what each tile contained (text cards or project thumbnails, as opposed to full-screen images), or whether the spiral loops.
- I could not verify the 30 May 2017 SOTD date on the Awwwards page itself. It comes from the search snippet only.
- I found no FWA or CSS Design Awards golden-spiral sites.

## Q3. CodePen / Observable / GitHub demos of golden-spiral, Fibonacci or golden-ratio zoom: how close are they?

### Takeaway
The closest demo is Nick Jones's own open-sourced "Scrolling Golden Spiral" (CodePen JNVyJb, mirrored as a GitHub Gist). It implements exactly rotate(90°·i) with scale(0.618^i) on scroll, keys, touch or click. It does **not** loop: rotation is clamped and there are 15 finite sections. A GeoGebra applet, "Zoom in Golden Rectangle (infinite loop)", shows the looping math, but it is not a website. Most other Fibonacci pens just draw the spiral.

### Cited Findings
- Gist "Scrolling Golden Spiral" (published 7 Jan 2019, credited to Nick Jones / narrowdesign, "used to create narrowdesign.com"). It has 15 `.js-section` divs. Each section gets `rotate(myRot deg) scale(Math.pow(aspect, i))` with aspect = 0.618033 and a spiral-origin "axis" of about 0.7237. The rotation is constrained between -1500° and 1200° by `trimRotation()`, so it does not loop infinitely. Input is scroll, arrow keys, touch, or clicking a section. VERIFIED — [gist.github.com/synecdocheNORTH/6c08dd959b532d5cdf710f4688ffe905](https://gist.github.com/synecdocheNORTH/6c08dd959b532d5cdf710f4688ffe905)
- The original CodePen is "Scrolling Golden Spiral" by narrowdesign. SNIPPET (page blocked) — [codepen.io/narrowdesign/pen/JNVyJb](https://codepen.io/narrowdesign/pen/JNVyJb)
- "Zoom in Golden Rectangle (infinite loop)" is a GeoGebra applet by Vincent Pantaloni: a looping mathematical zoom into the golden rectangle. SNIPPET — [geogebra.org/m/wXXc5cQ9](https://www.geogebra.org/m/wXXc5cQ9)
- The following draw or animate a Fibonacci spiral and do not navigate: SVG Fibonacci/golden spiral (myidealab), "Animated Fibonacci Growing Spiral – CSS" (josetxu), p5.js versions (RedHenDev, w4ctech), "Animated Fibonacci Spiral" (thehack), Coding Challenge "Infinite Fibonacci Spiral in p5.js" (YouTube), and sahasatvik's polar Fibonacci zoom-out. SNIPPET — [myidealab](https://codepen.io/myidealab/pen/NrgjdK); [josetxu](https://codepen.io/josetxu/pen/MYwxGMp); [RedHenDev](https://codepen.io/RedHenDev/pen/MmGGXW); [w4ctech](https://codepen.io/w4ctech/pen/ELqpdQ); [thehack](https://codepen.io/thehack/pen/PzaarZ); [YouTube](https://www.youtube.com/watch?v=uQXUazMvSCw); [sahasatvik](https://sahasatvik.github.io/fibonacci_spiral/)
- Codrops "ScrollSpiral" is a WebGL/regl decorative spiral background on scroll. It is spiral-themed but not golden-rectangle navigation. SNIPPET — [github.com/codrops/ScrollSpiral](https://github.com/codrops/ScrollSpiral)
- The Unity Zoom-Quilt gist turns z-position into card scaling. It is a generic infinite-zoom implementation. SNIPPET — [steve-salmond gist](https://gist.github.com/steve-salmond/5952537)

### Inferences
- In code terms, the concept is "Jones's spiral + modulo wrap". Because scale(φ) with rotate(90°) maps the subdivision onto itself, you can reset the index after N steps (keeping only a few nested layers alive) and get a seamless loop, the same trick Zoomquilt uses. Jones's demo clamps rotation instead, so the infinite loop is a real, if small, technical difference.

### Gaps
- I could not search Observable directly and found no Observable notebook on golden-spiral zoom navigation.
- I could not open CodePen to check for forks of JNVyJb that add looping or full-screen images.

## Q4. Brand campaigns or agency sites using spiral/zoom scroll as the main navigation (Prezi-style, ZUI)?

### Takeaway
Zooming user interfaces (ZUIs) are an established GUI paradigm (Prezi is the best-known consumer example). Zoom-into-image scroll transitions are a common Awwwards pattern. Apart from narrowdesign.com, I found no brand or agency site that uses golden-spiral zoom as its main navigation.

### Cited Findings
- A ZUI is a GUI where users change the scale of the view on an "infinite virtual desktop" and pan or zoom into objects. SNIPPET — [Wikipedia: Zooming user interface](https://en.wikipedia.org/wiki/Zooming_user_interface)
- Awwwards "infinite scroll" collections and inspiration entries include zoom-in scroll navigation (Ocus), infinite-scroll portfolio pages (Akufen Studio, Arvin Leeuwis), and recent infinite-scroll SOTDs such as Gionatan Nese '26 (SOTD 5 Sep 2026) and Loop Creative Studio (27 Aug 2026). These are generic infinite or zoom scroll, not golden geometry. SNIPPET — [Awwwards infinite-scroll collection](https://www.awwwards.com/websites/infinite-scroll/); [Akufen](https://www.awwwards.com/inspiration/portfolio-project-page-infinite-scroll-navigation-akufen-studio); [Arvin Leeuwis](https://www.awwwards.com/inspiration/infinite-scroll-homepage); [Ocus](https://www.awwwards.com/inspiration/scroll-navigation-zoom-in-effect-ocus)
- Codrops has many scroll-driven WebGL galleries and infinite-tube tutorials (for example, a scroll-reactive 3D gallery, Mar 2026). SNIPPET — [Codrops 2026-03-09](https://tympanus.net/codrops/2026/03/09/building-a-scroll-reactive-3d-gallery-with-three-js-velocity-and-mood-based-backgrounds/); [Codrops "infinite" tag](https://tympanus.net/codrops/tag/infinite/)

### Inferences
- Infinite scroll and zoom transitions are common in 2025–2026 award sites. Golden-spiral rotation-and-zoom navigation remains rare: the only documented case is one well-known 2017 site.

### Gaps
- I did not find any brand campaign (as opposed to a portfolio) using golden-spiral navigation. Behance, Dribbble, It's Nice That, Dezeen and Creative Boom were not searched individually because of the tool-call budget and blocked domains.

## Q5. How close is the closest precedent to the full concept?

### Takeaway
narrowdesign.com (2017) matches the core mechanic: scroll-driven zoom into golden-rectangle squares, ×φ with 90° rotation, as a designer's portfolio. As far as could be checked, it differs in three ways. (a) It is finite and clamped, not an endless loop. (b) Its tiles were mixed content cards (text and project tiles), not one full-bleed image per step (unverified). (c) It had a patterned and typographic look, not an ultra-minimal industrial-design aesthetic. Zoomquilt/Arkadia supply the endless-loop half, but with no golden geometry and no rotation.

### Cited Findings
- Matches: "zooming from one square to the next and rotating 90 degrees… an infinitely deep interface" (Jones). SNIPPET — [Fast Company 2017](https://www.fastcompany.com/90125529/7-design-portfolios-that-double-as-awesome-uis)
- Not looping: rotation is clamped to the range -1500° to 1200°, with 15 sections. VERIFIED — [Gist](https://gist.github.com/synecdocheNORTH/6c08dd959b532d5cdf710f4688ffe905)
- Loop technique precedent: the Zoomquilt "last card is the one before the first" structure. SNIPPET — [steve-salmond gist](https://gist.github.com/steve-salmond/5952537)
- Mathematical loop precedent: GeoGebra "Zoom in Golden Rectangle (infinite loop)". SNIPPET — [GeoGebra](https://www.geogebra.org/m/wXXc5cQ9)

### Inferences
- Closeness rating: about 70–80% of the concept's core navigation idea was publicly done, open-sourced and award-recognised in 2017. The remaining differences are the seamless infinite loop, one full-screen image per square (each square works as a "slide"), and minimal industrial-design art direction. These are refinements of execution, not a new paradigm.
- Recommendation for positioning: treat narrowdesign.com as a known reference to acknowledge or build on, not something to hide. Present the difference as "endless, image-led, reduced and calm". Plan for the vertigo criticism the 2017 site received (slower easing, reduced-motion fallback).

### Gaps
- I could not confirm the current state of narrowdesign.com (live spiral or not, in 2026), or whether its tiles ever held full-screen photography.
- I could not confirm whether any 2018–2026 site has combined golden-spiral zoom with a seamless loop. Search found none, but CodePen, Awwwards and Behance could not be browsed directly.
