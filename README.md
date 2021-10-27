![logoslogan](https://user-images.githubusercontent.com/56782487/138986594-54a85c97-9381-45c6-a8ff-ee7893cecca4.png)

# Audiobook-Engine

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
<h1>Prerequisites:</h1>
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

<h1>Processes:</h1>
<h3>Background Noise Reduction</h3>
<img src="https://user-images.githubusercontent.com/56782487/138979962-dba3ca2c-3bc7-4bee-a8fd-26ee294de81c.png" width="60%">
Background Noise Reduction scans the audiobook for periods of “silence” and analyses the background noise. It then equalizes the whole audiobook to reduce the background noise. Although it is possible to completely remove the background noise with this tool, a total reduction can leave the dialogue sounding quite bad. But, a more subtle use of the Background Noise Reduction along with Silence Skipping can go a long way to reduce the effects of the background noise. I'd say that for most audiobooks ripped from cassettes, this is the most important feature.

The only adjustable value on this page is noise reduction amount, which is pretty self explanatory. A lower percentage will do less to reduce the background noise, and vice versa.

<br>
<h3>Compression</h3>
<img src="https://user-images.githubusercontent.com/56782487/138980333-8ba6351f-dc09-48fa-91cd-b0c54e931264.PNG" width="60%">

Compression makes it so that there aren’t large changes in volume throughout the course of the audiobook. It does this by detecting any parts of the audio that go over a certain volume and reducing the volume of those parts. Compression will leave your audiobook overall quieter than it was before, so it’s recommended that you use volume normalisation at the same time to bring the volume back up.

There are four controls on the compression page:<br>
<div><ul>
	<li>Threshold is the volume that audio has to go over to be affected by the compressor. Set this lower if the compressor doesn't seem to be doing anything and higher if all it's doing is making the audio quieter (it will be quieter overall anyway)</li>
	<li>Ratio is the amount the volume will be reduced by when part of the audiobook goes over the volume set by the Threshold. Set this number higher to make the compressor more effective, but having it too high can sound weird, so use with caution.</li>
	<li>The attack specifies how long it takes the compressor to lower the volume by the ratio specified by the ratio box after it goes over the volume specified in the threshold box. Setting this number lower makes the volume more consistent, but it makes the volume changes very unnatural sounding.</li>
	<li>The release specifies how long it takes the compressor to turn off after the volume of the audiobook goes below the threshold. Having this number too low can make parts of the audiobook quieter that you would like, but too high can sound unnatural.			
</ul></div>

On the internet there are a lot of guides on how to use an audio compressor that are far more comprehensive than mine, so look at some of those if you want to know more.

<br>
<h3>Volume Normalisation</h3>
<img src="https://user-images.githubusercontent.com/56782487/138981581-6d50d61f-9be5-42d0-8dfc-f34301fd2453.PNG" width="60%">

Normalisation changes the overall volume of the audiobook to match a goal volume (by default, 0.0 dB). This can be useful for bringing the volume up after an audiobook has had compression; if the audiobook was just recorded quietly to begin with; or if different files from the same audiobook are at different volumes.

There is only one input for normalisation and it's the target volume that the audio will be normalised to. 0dB is normally the maximum volume that you can have an audio file at before it starts causing problems such as clipping, so I recommend just keeping it at that. Lowering the value will give you a quieter file and raising it will give you a louder file.
	
<br>
<h3>Vocal EQ</h3>
<img src="https://user-images.githubusercontent.com/56782487/138984795-c46fc9a4-e692-4bba-aa32-c4651456f535.PNG" width="60%">

This Equaliser is for making any adjustments to the way vocals sound on the recording. This could be used for reducing boom from lower voices, softening higher pitched voices, reducing nasality, or a bunch of other things. It does this by raising or lowering the volume of different frequencies in the audiobook.

There is only one input for the equaliser, but it's repeated ten times. Each slider raises or lowers the frequency listed, and the surrounding frequencies, by the amount selected.

<br>
<h3>Silence Skipping</h3>
<img src="https://user-images.githubusercontent.com/56782487/138987490-e2d570ed-20fc-400b-94f5-f12b87e71f22.PNG" width="60%">

Silence skipping detects periods of silence in audiobooks and reduces them. There will still be short periods of silence left, so that the audiobook still sounds natural and non-fatiguing. 

There are four controls on the Silence Skipping page:<br>
<div><ul>
	<li>The Minimum Silence is how long a period of silence has to be before it will be shortened. Raising this value will mean that periods of silence have to be longer before they will be removed, and vice versa.</li>
	<li>The Silence Threshold is the volume that the audio has to go below before it counts as silence. If the silence skipping doesn't appear to be working, try raising this value. If too much is being skipped (including the beginnings and ends of words) try lowering this value.</li>
	<li>The Keep Silence value tells the program how much silence to keep when silence is being skipped. This helps prevent there being absolutely no silence in the audiobook, which can sound fatiguing.</li>
	<li>The Searching Step value controls how often the program checks to see if the audiobook is silent or not. For example, if Seek Step is set to 5ms, it will check for silence every five milliseconds. The only reason to raise this number is to make the program run quicker.</li>
</ul></div>

<h1>Planned features</h1>
<div><ul>
	<li>Dolby Noise Reduction Decoding</li>
	<li>Mouth Noise Reduction</li>
</ul></div>

<h1>Licence</h1>
<a href="https://tldrlegal.com/license/mit-license">MIT</a>
