![logoslogan](https://user-images.githubusercontent.com/56782487/138986594-54a85c97-9381-45c6-a8ff-ee7893cecca4.png)

# Audiobook Engine

Audiobook Engine is a piece of software designed to make the restoration of audiobooks simple and achievable for everyone.

Hear samples of Audiobook Engine in action <a href='https://richardmosen.com/audiobookenginesamples'>here.</a>

<h3>Table of Contents</h3>
<div><ul>
	<li><a href="#Background">Background</a></li>
	<li><a href="#FeatureOverview">Feature Overview</a></li>
	<li><a href="#Prerequisites">Prerequisites</a></li>
	<li><a href="#Processes">Processes</a></li>
	<div><ul>
		<li><a href="#BackgroundNoiseReduction">Background Noise Reduction</a></li>
		<li><a href="#Compression">Compression</a></li>
		<li><a href="#VolumeNormalisation">Volume Normalisation</a></li>
		<li><a href="#VocalEQ">Vocal EQ</a></li>
		<li><a href="#SilenceSkipping">Silence Skipping</a></li>
	</ul></div>
	<li><a href="#PlannedFeatures">Planned Features</a></li>
	<li><a href="#Licence">Licence</a></li>
	<li><a href="#Sources">Sources</a></li>
</ul></div>

<audio controls>
  <source src="https://github.com/RMosen/Audiobook-Engine/blob/main/Sample%20Audiobooks/DarkTowerSSkip.mp3" type="audio/mpeg">
  <!-- fallback for non supporting browsers goes here -->
  <p>Your browser does not support HTML5 audio, but you can still
     <a href="https://github.com/RMosen/Audiobook-Engine/blob/main/Sample%20Audiobooks/DarkTowerSSkip.mp3">download the music</a>.</p>
</audio>

<h1 id="Background">Background</h1>

Thousands of audiobooks have only ever been released on cassette, and cassettes degrade over time. Eventually, those cassettes will be unlistenable, and the audiobooks that have never been digitised will be lost [[1]](#1) . That’s why I created Audiobook Engine. Built to be easy to use, Audiobook Engine is designed to help anyone remove the damage that time has done to audiobooks, and sometimes make them sound better than ever before.

Even though it’s easy to digitise audiobooks and, with the help of software like Audiobook Engine, restore the sound quality, there are still big problems with the preservation of audiobooks due to copyright laws. Even if I were to restore a whole library of audiobooks, that would only benefit me due to it being illegal for me to distribute them online.

Eventually, all these audiobooks will fall into the public domain, but by that point it’s likely that most of the cassettes they’re stored on will be heavily degraded. That’s why it’s important to digitise any audiobooks you might have on cassette and keep them safe.

As far as I know there’s no database online of what audiobooks have been digitised for private use (because that would be a very niche database). So, my advice is to digitise any audiobooks you have, otherwise they could be lost for future generations.

<h1 id="FeatureOverview">Feature Overview</h1>

Audiobook Engine does not currently preform the initial task of digitising your cassettes (How-To Geek has <a href='https://www.howtogeek.com/177084/how-to-digitizebackup-cassette-tapes-and-other-old-media/'>a great guide</a> on how to do that though). What it does do is take the audio files that you have generated through digitising your cassettes and helps you to get them sounding good as new.

I’ve spent a lot of time in the past restoring audiobooks manually through a DAW, and through my own experience I’ve managed to determine the best ways to restore audiobooks. Although Audiobook Engine can’t replicate the precision of manually restoring an audiobook, it allows you to get most of the way there in a fraction of the time with a fraction of the effort.

I’ve boiled the process of restoring almost any audiobook down into five simple to use tools. They are:
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
	<li>Diverse Inbuilt Presets</li>
	<li>Helpful Info Boxes</li>
</ul></div>

<h1 id="Prerequisites">Prerequisites:</h1>
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

<h1 id="Processes">Processes:</h1>

You can hear samples of all of these processes in action <a href='https://richardmosen.com/audiobookenginesamples'>here.</a>

<h3 id="BackgroundNoiseReduction">Background Noise Reduction</h3>
<img src="https://user-images.githubusercontent.com/56782487/138979962-dba3ca2c-3bc7-4bee-a8fd-26ee294de81c.png" width="60%">
Background Noise Reduction scans the audiobook for periods of “silence” and analyses the background noise. It then equalizes the whole audiobook to reduce the background noise. Although it is possible to completely remove the background noise with this tool, a total reduction can leave the dialogue sounding quite bad. But, a more subtle use of the Background Noise Reduction along with Silence Skipping can go a long way to reduce the effects of the background noise. I'd say that for most audiobooks ripped from cassettes, this is the most important feature.

The only adjustable value on this page is noise reduction amount, which is pretty self explanatory. A lower percentage will do less to reduce the background noise, and vice versa.

<br>
<h3 id="Compression">Compression</h3>
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
<h3 id="VolumeNormalisation">Volume Normalisation</h3>
<img src="https://user-images.githubusercontent.com/56782487/138981581-6d50d61f-9be5-42d0-8dfc-f34301fd2453.PNG" width="60%">

Normalisation changes the overall volume of the audiobook to match a goal volume (by default, 0.0 dB). This can be useful for bringing the volume up after an audiobook has had compression; if the audiobook was just recorded quietly to begin with; or if different files from the same audiobook are at different volumes.

There is only one input for normalisation and it's the target volume that the audio will be normalised to. 0dB is normally the maximum volume that you can have an audio file at before it starts causing problems such as clipping, so I recommend just keeping it at that. Lowering the value will give you a quieter file and raising it will give you a louder file.
	
<br>
<h3 id="VocalEQ">Vocal EQ</h3>
<img src="https://user-images.githubusercontent.com/56782487/138984795-c46fc9a4-e692-4bba-aa32-c4651456f535.PNG" width="60%">

This Equaliser is for making any adjustments to the way vocals sound on the recording. This could be used for reducing boom from lower voices, softening higher pitched voices, reducing nasality, or a bunch of other things. It does this by raising or lowering the volume of different frequencies in the audiobook.

There is only one input for the equaliser, but it's repeated ten times. Each slider raises or lowers the frequency listed, and the surrounding frequencies, by the amount selected.

<br>
<h3 id="SilenceSkipping">Silence Skipping</h3>
<img src="https://user-images.githubusercontent.com/56782487/138987490-e2d570ed-20fc-400b-94f5-f12b87e71f22.PNG" width="60%">

Silence skipping detects periods of silence in audiobooks and reduces them. There will still be short periods of silence left, so that the audiobook still sounds natural and non-fatiguing. 

There are four controls on the Silence Skipping page:<br>
<div><ul>
	<li>The Minimum Silence is how long a period of silence has to be before it will be shortened. Raising this value will mean that periods of silence have to be longer before they will be removed, and vice versa.</li>
	<li>The Silence Threshold is the volume that the audio has to go below before it counts as silence. If the silence skipping doesn't appear to be working, try raising this value. If too much is being skipped (including the beginnings and ends of words) try lowering this value.</li>
	<li>The Keep Silence value tells the program how much silence to keep when silence is being skipped. This helps prevent there being absolutely no silence in the audiobook, which can sound fatiguing.</li>
	<li>The Searching Step value controls how often the program checks to see if the audiobook is silent or not. For example, if Seek Step is set to 5ms, it will check for silence every five milliseconds. The only reason to raise this number is to make the program run quicker.</li>
</ul></div>

<h1 id="PlannedFeatures">Planned Features</h1>
<div><ul>
	<li>Dolby Noise Reduction Decoding</li>
	<li>Mouth Noise Reduction</li>
	<li>Metadata Support</li>
</ul></div>

<h1 id="Licence">Licence</h1>
<a href="https://tldrlegal.com/license/mit-license">MIT</a>

<h1 id="Sources">Sources:</h1>

<p id="1">[1] Schuller, D. (2001). Preserving the Facts for the Future: Principles and Practices for the Transfer of Analog Audio Documents into the Digital Domain. JAES, 49(7/8), 618–621.</p>
