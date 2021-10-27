# Audiobook-Engine

![logoslogan](https://user-images.githubusercontent.com/56782487/138986594-54a85c97-9381-45c6-a8ff-ee7893cecca4.png)


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
<b>Built with:</b>
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

<b>Features</b>

<br>
<b>Background Noise Reduction</b>
<img src="https://user-images.githubusercontent.com/56782487/138979962-dba3ca2c-3bc7-4bee-a8fd-26ee294de81c.png" width="60%">

Background Noise Reduction scans the audiobook for periods of “silence” and analyses the background noise. It then equalizes the whole audiobook to reduce the background noise. Although it is possible to completely remove the background noise with this tool, a total reduction can leave the dialogue sounding quite bad. But, a more subtle use of the Background Noise Reduction along with Silence Skipping can go a long way to reduce the effects of the background noise. I'd say that for most audiobooks ripped from cassettes, this is the most important feature.

The only adjustable value on this page is noise reduction ammount, which is pretty self explainitory. A lower percentage will do less to reduce the background noise, and vice versa.

<br>
<b>Compression</b><br>
<img src="https://user-images.githubusercontent.com/56782487/138980333-8ba6351f-dc09-48fa-91cd-b0c54e931264.PNG" width="60%">

Compression makes it so that there aren’t large changes in volume throughout the course of the audiobook. It does this by detecting any parts of the audio that go over a certain volume, and reducing the volume of those parts. Compression will leave your audiobook overall quieter than it was before, so it’s recommended that you use volume normalisation at the same time to bring the volume back up.

There are four controls on the compression page:<br>
<div><ul>
	<li>Threshold is the volume that audio has to go over to be effected by the compressor. Set this lower if the compressor doesn't seem to be doing anything and higher if all it's doing is making the audio quieter (it will be quieter overall anyway)</li>
	<li>Ratio is the ammount the voulme will be reduced by when part of the audiobook goes over the volume set by the Threshold. Set this number higher to make the compressor more effective, but having it too high can sound weird, so use with caution.</li>
	<li>The attack specifies how long it takes the compressor to lower the volume by the ratio specified by the ratio box after it goes over the volume specified in the threshold box. Setting this number lower makes the volume more consistent, but it makes the volume changes very unnatural sounding.</li>
	<li>The release specifies how long it takes the compressor to turn off after the volume of the audiobook goes below the threshold. Having this number too low can make parts of the audiobook quieter that you would like, but too high can sound unnatural.			
</ul></div>

On the internet there are a lot of guides on how to use an audio compressor that are far more comprehensive than mine, so look at some of those if you want to know more.

<br><br>
<b>Volume Normalisation</b><br>
<img src="https://user-images.githubusercontent.com/56782487/138981581-6d50d61f-9be5-42d0-8dfc-f34301fd2453.PNG" width="60%">

Normalisation changes the overall volume of the audiobook to match a goal volume (by default, 0.0 dB). This can be useful for bringing the volume up after an audiobook has had compression; if the audiobook was just recorded quietly to begin with; or if different files from the same audiobook are at different volumes.

There is only one input for normalisation and it's the target volme that the audio will be normalised to. 0dB is normally the maximum volume that you can have an audio file at before it starts causing problems such as clipping, so I recomend just keeping it at that. Lowering the value will give you a quieter file and raising it will give you a louder file.
	
<br><br>
<b>Vocal EQ</b><br>
<img src="https://user-images.githubusercontent.com/56782487/138984795-c46fc9a4-e692-4bba-aa32-c4651456f535.PNG" width="60%">

This Equaliser is for making any adjustments to the way vocals sound on the recording. This could be used for reducing boom from lower voices, softening higher pitched voices, reducing nasality, or a bunch of other things. It does this by raising or lowering the volume of different frequencies in the audiobook.

-Silence Skipping

	Silence skipping detects periods of silence in audiobooks and reduces them. There will still be short periods of silence left, so that the audiobook still sounds natural and (hopefully) not fatiguing. 

	Silence skipping is powered by PyDub

---Planned features
	- Dolby Noise Reduction

---Licence
	-GNU General Public License v3.0
