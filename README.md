# vocf
Scripts and data created for the purpose of visualizing the Oregon Country Fair site in 3D, using LIDAR scans from the USGS National Map.
05/02/2020

########################################################
###     Welcome to the Virtual OCF Site project      ###
###                 By Chris Calef                   ###
########################################################

Hi, and thanks for checking out this project! My name is Chris, I've been coming to Fair for eight years, I work Peach Gate bag check security from 3:30 to 9:30, and I am very sad about us all having to skip it this year. :-(

Given the situation, I'm sure a lot of people are thinking about what an online Oregon Country Fair might look like. I know I have been. I imagine there will be as many suggestions as there are people, but here is mine.

For me, the site is the most important part of the fair. This isn't an event that takes place in hotels, this is an event very deeply tied to the ground on which it happens. And as a 3D game programmer, I would find it tragic if July 2020 rolled around and there was no 3D virtual site to stroll around in. (At least for the people who are into that sort of thing.)

I am sure that there will be many fairgoers who won't be interested in attending anything that isn't a physical fair, and maybe others for whom zoom meetups or chat rooms will be sufficient, but for me the coolest thing about Fair is the random meetings that happen when you see somebody on the Eight that you haven't seen in years, and get a chance to catch up and have a hug. Obviously we can't do the hugs, and the random meetups are going to be made much more difficult by the fact that we can't see each other's faces, but in the absense of other known alternatives, I would like to propose here a mechanism by which interested parties might at least have a _chance_ of randomly meeting up with each other. And everybody would get at least some shadow of the experience of walking around the Eight.

In addition, it is very important to me that the craft vendors and musicians, and anyone else who can fit into this paradigm, be given a chance to circulate their wares among Fair attendees and hopefully make some sales out of it.

There are many ways by which a site as large as the OCF land could be presented in 3D. I expect much conversation on this subject, but after considering the time frame (two months) and available resources (none so far, except my time) I have come to the initial conclusion that we might be wisest to make use of Mozilla Hubs.

There are many drawbacks to this platform, as compared to some other options, like:

  1) writing an app in Unity

  2) making use of existing games/online environments like Minecraft or Second Life

  3) ...?

The drawbacks of Hubs are mostly related to performance on phones, but for people used to MMO games, they are going to feel quite limiting: somewhere around 25 avatars in a room is the first and most painful one, also the limits of around 50000 polygons and 25 distinct materials are quite uncomfortable for anyone used to working in a game environment like Unity.

My strategy for dealing with these limits is to A) break up the site into a 5x5 grid (or another structure that results in tiles of a similar size) so as to present some detail within the poly limits, and B) allow Hubs to make copies of rooms when they fill up (I think that is how it works) so even though there may only be 25 people in a given room, there could be hundreds of copies of that room at the same time.

The reason I am leaning toward this somewhat awkward solution is threefold:

  1) we only have two months to create a playable environment, which is not a lot of time to write an MMO

  2) if we write our own thing, we would have to host it and be sure it can deal with the traffic on the fateful weekend, whereas using Hubs we can probably trust Mozilla to have big enough servers to deal with us

  3) the OCF family is made up a large number of people who, especially in the elder community, may not be the most tech savvy collection of individuals on the face of the planet. The goal of any virtual OCF should be to involve as many of the Fair Family as possible, and as someone who works in a company which makes a Unity app, I can tell you that the "download my app" barrier is very real. The fact is, nobody wants to download your app, they don't know you and don't trust you and would just rather not. Hubs is based in your browser and it just takes clicking on a link (well, plus a few permissions clicks) and you are right in the room.

Whatever vehicle we end up using to present the 3D fair site, though, the initial problem remains: that of creating the 3D model. That is the goal of this repository.

The rest of this document will be devoted to technical details.

#######################################################

So, down to the nitty gritty!

First, tools you will want to download if you wish to replicate this process. Given that I have an enduring interest in GIS tools and LIDAR scans, when confronted with this problem I went straight there. Aside from Python these are the tools I used to get from the very large USGS pointcloud down to a reasonable set of 5x5 grid tiles, with forest canopy meshes:

1) CloudCompare:  http://www.danielgm.net/cc/release/

   This is a very useful tool for visualizing and cropping point clouds, and I also used it to filter out the ground points and leave me with the forest canpoy.

2) MeshLab:  http://www.meshlab.net/

   This is for resampling, generating normals, and tesselating (putting a mesh around) the point sets. I use it to import ply files, and export .obj files.

3) Blender:  http://blender.org

   The ubiquitous free 3D modeling (and so much more) software that you can't live without, if you are broke and want to get into 3D modeling. I use this to import .obj files created in MeshLab, and export .glb files that I can import into Hubs.

Outside of these, all you need is a python interpreter, if you want to get into the code.

########################################################

Now, to the code. I ended up writing a small set of python scripts:

  chop_grid.py - This is reducing the initial pointcloud crop, containing the entire site, into a 5x5 grid of smaller pointclouds.

  center_rot_pos.py - This is for rotating and centering each grid tile, to get the points based around their local origin and to flip the orientation from left handed, Y up, the way it comes in, to right handed Z up for Blender and Hubs.

  meshlab_grid.py - Particularly happy with how this turned out: this is a script that automates the process of using MeshLab to sample, filter, and meshify (tesselate) each pointcloud, and save it out as an obj. It uses "canopy_script.mlx" as a filter file.

  find_trees.py - this is a work in progress, but it is an attempt to run through each pointcloud, and by analysis of point heights and normals, attempt to identify positions of individual trees, so that a tree trunk model can be appropriately placed on the ground.

find_trees.py makes use of the extremely powerful scipy/spatial/kdtree.py, which implements a K-dimensional binary search tree algorithm. You feed it a cloud of points, and it organizes them into a structure which can search for near neighbors very efficiently.





