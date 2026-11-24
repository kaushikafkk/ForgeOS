import QtQuick 2.15
import QtQuick.Layouts 1.15
import org.kde.kirigami 2.20 as Kirigami
import org.kde.plasma.components 3.0 as PlasmaComponents3
import org.kde.plasma.plasmoid 2.0

PlasmoidItem {
    id: root
    Plasmoid.icon: "forgeos"
    Plasmoid.preferredRepresentation: Plasmoid.fullRepresentation

    Plasmoid.fullRepresentation: RowLayout {
        spacing: 12
        Layout.minimumWidth: 280
        Layout.preferredWidth: 310
        Layout.fillHeight: true

        Kirigami.Icon {
            source: "forgeos"
            Layout.preferredWidth: 28
            Layout.preferredHeight: 28
        }

        Rectangle {
            Layout.preferredWidth: 1
            Layout.preferredHeight: 25
            color: "#53636d"
            opacity: 0.7
        }

        PlasmaComponents3.Label {
            text: "Workspace 01  ·  Backend"
            color: "#f4f7f9"
            font.pixelSize: 15
            font.weight: Font.DemiBold
            Layout.fillWidth: true
        }
    }
}
