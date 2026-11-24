import QtQuick
import QtQuick.Layouts
import org.kde.kirigami as Kirigami
import org.kde.plasma.components as PlasmaComponents3
import org.kde.plasma.plasmoid

PlasmoidItem {
    id: root
    Plasmoid.icon: "forgeos"
    Plasmoid.preferredRepresentation: Plasmoid.fullRepresentation
    Layout.minimumWidth: 280
    Layout.preferredWidth: 310
    Layout.fillHeight: true
    implicitWidth: 310

    RowLayout {
        anchors.fill: parent
        spacing: 12

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
