# ForgeOS desktop design contract

The desktop concept in `docs/screenshots/forgeos-desktop-concept.png` is the visual target for the native ForgeOS session. It is not treated as a browser mockup or as a substitute for implementation evidence.

## Native mapping

| Design element | Native implementation |
| --- | --- |
| Teal/orange contour background | Scalable ForgeOS SVG wallpaper |
| Upper-left ForgeOS identity | Plasma 6 `org.forgeos.brand` widget |
| Centered workspace capsule | Floating Plasma panel with the `org.forgeos.workspace` widget, system tray, and clock |
| Vertical launcher | Floating Plasma icon-task panel with Forge Shell, Files, Firefox, Discover, Forge Hub, and Settings |
| Developer terminal | Konsole with the ForgeOS profile, JetBrains Mono, dark translucent palette, and colored shell prompt |
| Forge Hub surface | Native GTK 4 application using the local `forged` Unix-socket API |
| Window composition | Adaptive KWin script that anchors Forge Shell left and Forge Hub right |

## Product truth

The concept contains future states such as automatic snapshots, transactional updates, and workspace creation. The native UI must not claim those mutations work before their backend, authorization, rollback, and fault tests exist. Current cards therefore show real system metrics and daemon health while presenting unfinished features as guarded or planned.

Every successful ISO build triggers the QEMU proof workflow. Release screenshots must come from that booted image, not from the concept file.
