# Audiobook-Engine

![logoslogan](https://user-images.githubusercontent.com/56782487/138974838-157e18d0-f6c3-4713-b925-e80b3420073d.png)


---About this project

	-Justification
	 This project aims to be a simple solution to restoring the sound quality of audiobooks. The main target is audiobooks recorded from cassettes, but it should be a fairly universal solution.

	-overview of functions
	This project utilises various pre-existing libraries to remove background hiss, poor volume mixing, unnecessary silences and other common problems with audiobooks. The goal is to make using these tools easy for anyone who doesn’t know a line of code, or a thing about audio production.

	-over-all a/b
	[embedded examples of audiobooks improved by the software]

---Prerequisites
	-PyDub
	-Librosa
	-PySimpleGui
	-NumPy
	-Soundfile
	-Noisereduce

--- Feature list
	-Volume Normalisation
	-Audio Compression
	-Background Noise Reduction
	-Mouth Noise Reduction
	-General EQ
	-Silence Skipping

---Expanding on each feature

-Audio Compression

	Compression makes it so that there aren’t large changes in volume throughout the course of the audiobook. It does this by detecting any parts of the audio that go over a certain volume, and reducing the volume of those parts. Compression will leave your audiobook overall quieter than it was before, so it’s recommended that you use volume normalisation at the same time to bring the volume back up.
	
	Audio compression is powered by PyDub.


-Volume Normalisation

	Normalisation changes the overall volume of the audiobook to match a goal volume (by default, -0.1 db). This can be useful for bringing the volume up after an audiobook has had compression; if the audiobook was just recorded quietly to begin with; or if different files from the same audiobook are at different volumes.

	Volume Normalisation is powered by PyDub

-Background Noise Reduction

	Background Noise Reduction scans the audiobook for periods of “silence” and analyses the background noise. It then equalizes the whole audiobook to reduce the background noise. Although it is possible to completely remove the background noise with this tool, a total reduction can leave the dialogue sounding quite bad. But, a more subtle use of the Background Noise Reduction along with Silence Skipping can go a long way to reduce the effects of the background noise.

	Background noise reduction is powered by NoiseReduce, with help from PyDub for isolating periods of silence.

-Mouth Noise Reduction
	

-General EQ
	
	This Equaliser is for making any adjustments to the way vocals sound on the recording. This could be used for reducing boom from lower voices, softening higher pitched voices, reducing nasality, or a host of other things. There are a variety of presets, but to get the best results it is possible to manually adjust the eq to any setting.

	This EQ is powered by PyDub

-Silence Skipping

	Silence skipping detects periods of silence in audiobooks and reduces them. There will still be short periods of silence left, so that the audiobook still sounds natural and (hopefully) not fatiguing. 

	Silence skipping is powered by PyDub

---Planned features
	- Dolby Noise Reduction

---Licence
	-GNU General Public License v3.0
