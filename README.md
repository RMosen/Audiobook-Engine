# Audiobook-Engine

![logoslogan](https://user-images.githubusercontent.com/56782487/138974838-157e18d0-f6c3-4713-b925-e80b3420073d.png)


Audiobook Engine is a tool for restoring the sound quality of audiobooks, with a particular focus on audiobooks ripped from cassettes.

It's audio processing features include:
<div><ul>
	<li>Noise Reduction</li>
	<li>Compression</li>
	<li>Volume Normalisation</li>
	<li>10 Band Equaliser</li>
	<li>Silence Skipping</li>
</ul></div>

As well as several quality of life improvements such as:
<div><ul>
	<li>Batch Processing</li>
	<li>In App Playback</li>
	<li>Diverse inbuilt presets</li>
	<li>Helpful info boxes</li>
</ul></div>

	-over-all a/b
	[embedded examples of audiobooks improved by the software]
Built with:
<div><ul>
	<li><a href="https://github.com/jiaaro/pydub">PyDub</a></li>
		Pydub is the backbone of this software. It handles importing/exporting audio as well as the compressor, normalisation,
		equalisation, silence skipping and audio playback.
	<li><a href="https://github.com/timsainb/noisereduce">noisereduce</a></li>
		Noisereduce runs the background noise reduction part of the software. It's very impressive how well it works.
	<li><a href="https://numpy.org/">NumPy</a></li>
		NumPy is needed to convert Pydub's audio segments into a format that noisereduce can understand.
	<li><a href="https://github.com/hamiltron/py-simple-audio">SimpleAudio</a></li>
		The way audio playback is handled in Audiobook Engine is with Simpleaudio via Pydub's playback feature. Sometimes it worked out better to control the
		audio directly through SimpleAudio, which is why it's here.
	<li><a href="https://pysimplegui.readthedocs.io/en/latest/">PySimpleGui</a></li>
		PySimpleGui handles the GUI for Audiobook Engine.
</ul></div>

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
