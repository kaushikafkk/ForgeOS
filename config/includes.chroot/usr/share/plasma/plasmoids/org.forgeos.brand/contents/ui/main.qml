import QtQuick
import QtQuick.Layouts
import org.kde.kirigami as Kirigami
import org.kde.plasma.components as PlasmaComponents3
import org.kde.plasma.plasmoid

PlasmoidItem {
    Plasmoid.icon: "forgeos"
    Plasmoid.preferredRepresentation: Plasmoid.fullRepresentation
    Layout.minimumWidth: 180
    Layout.preferredWidth: 200
    Layout.fillHeight: true
    implicitWidth: 200

    RowLayout {
        anchors.fill: parent
        spacing: 10

        Kirigami.Icon {
            source: "forgeos"
            Layout.preferredWidth: 31
            Layout.preferredHeight: 31
        }
        PlasmaComponents3.Label {
            text: "Forge"
            color: "#f4f7f9"
            font.pixelSize: 21
            font.weight: Font.Bold
        }
        PlasmaComponents3.Label {
            text: "OS"
            color: "#ffab32"
            font.pixelSize: 21
            font.weight: Font.Bold
            Layout.leftMargin: -10
        }
    }
}
